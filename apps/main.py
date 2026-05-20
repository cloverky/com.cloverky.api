import asyncio
import json
import logging
import re
import sys

# Windows: psycopg async + uvicorn 시 DB 요청이 멈추는 문제 방지
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
import urllib.error
import urllib.parse
import urllib.request
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from matrix.app.keymaker import get_keymaker

from adapters.db_health_adapter import DbHealthAdapter
from fridge.models.database import Base, dispose_engine, engine, get_db
from models.user import User, UserRole  # noqa: F401 — create_all 에 테이블 등록
from models.ingredient_manager import IngredientManager  # noqa: F401
from fridge.models.category_model import FridgeCategory  # noqa: F401
from fridge.models.code_model import FridgeCode  # noqa: F401
from fridge.models.food_model import FridgeFood  # noqa: F401
from fridge.models.inventory_model import FridgeInventory  # noqa: F401
from fridge.models.user import FridgeUser  # noqa: F401
from fridge.controllers.ingredient_router import router as inventory_router
from doro.app.doro_director import DoroDirector
from titanic.app.james_controller import JamesController
from secom.app.schemas.user_schema import LoginSchema, UserSchema
from secom.app.controllers.user_controller import UserController

keymaker = get_keymaker()
logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


class ChatRequest(BaseModel):
    """채팅 요청 본문. 사용자 메시지를 JSON으로 전달합니다."""

    message: str = Field(..., min_length=1, description="사용자 메시지")


class ChatResponse(BaseModel):
    reply: str


class WeatherResponse(BaseModel):
    city: str
    country: str
    temp_c: float
    feels_like_c: float
    description: str
    icon: str
    humidity: int


class SignUpRequest(BaseModel):
    """회원가입 요청 — JSON 본문 (camelCase 필드명 지원)."""

    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(..., min_length=1, description="이름")
    username: str = Field(..., min_length=2, max_length=20, description="아이디")
    email: str = Field(..., min_length=3, description="이메일")
    password: str = Field(..., min_length=8, description="비밀번호")
    confirm_password: str = Field(
        ...,
        min_length=8,
        alias="confirmPassword",
        description="비밀번호 확인",
    )
    agree_terms: bool = Field(..., alias="agreeTerms", description="약관 동의")

    @field_validator("username")
    @classmethod
    def username_format(cls, v: str) -> str:
        u = v.strip()
        if not re.fullmatch(r"[a-zA-Z0-9_]{2,20}", u):
            raise ValueError("아이디는 2~20자의 영문, 숫자, _ 만 사용할 수 있습니다.")
        return u

    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("올바른 이메일 형식이 아닙니다.")
        return v.strip()


class SignUpResponse(BaseModel):
    message: str
    username: str
    email: str


class LoginRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    email: str = Field(..., min_length=3)
    password: str = Field(..., min_length=8)
    remember: bool = Field(default=False, description="로그인 상태 유지")


class LoginResponse(BaseModel):
    message: str
    name: str
    username: str
    email: str


class UsernameCheckResponse(BaseModel):
    username: str
    available: bool
    message: str


def _username_key(username: str) -> str:
    return username.strip().lower()


async def _ensure_entity_rule_schema(conn) -> None:
    """ENTITY_RULE.md: PK는 int 자동증감 `id`, 레거시 secom_users 제거."""
    await conn.execute(text("DROP TABLE IF EXISTS secom_users CASCADE"))
    await conn.execute(
        text(
            """
            DO $$
            DECLARE
              tbl text;
            BEGIN
              FOREACH tbl IN ARRAY ARRAY[
                'users',
                'ingredient_manager',
                'fridge_categories',
                'fridge_foods',
                'fridge_codes',
                'fridge_inventory',
                'fridge_users'
              ]
              LOOP
                IF EXISTS (
                  SELECT 1 FROM information_schema.tables
                  WHERE table_schema = 'public' AND table_name = tbl
                ) AND NOT EXISTS (
                  SELECT 1 FROM information_schema.columns
                  WHERE table_schema = 'public'
                    AND table_name = tbl
                    AND column_name = 'id'
                ) THEN
                  EXECUTE format(
                    'ALTER TABLE %I ADD COLUMN id SERIAL PRIMARY KEY', tbl
                  );
                END IF;
              END LOOP;
            END $$;
            """
        ),
    )


async def _migrate_tables() -> None:
    """users·ingredient_manager 테이블 생성 및 ENTITY_RULE·스키마 보강."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await _ensure_entity_rule_schema(conn)
        await conn.execute(
            text(
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(20) "
                "NOT NULL DEFAULT 'user'"
            ),
        )
        # 기존 Neon 테이블명 inventory_items → ingredient_manager
        await conn.execute(
            text(
                """
                DO $$
                BEGIN
                  IF EXISTS (
                    SELECT 1 FROM information_schema.tables
                    WHERE table_schema = 'public' AND table_name = 'inventory_items'
                  ) AND NOT EXISTS (
                    SELECT 1 FROM information_schema.tables
                    WHERE table_schema = 'public' AND table_name = 'ingredient_manager'
                  ) THEN
                    ALTER TABLE inventory_items RENAME TO ingredient_manager;
                  END IF;
                END $$;
                """
            ),
        )
        await conn.execute(
            text(
                "ALTER TABLE ingredient_manager "
                "ADD COLUMN IF NOT EXISTS purchased_date DATE"
            ),
        )
        await conn.execute(
            text(
                "ALTER TABLE ingredient_manager "
                "ADD COLUMN IF NOT EXISTS expiry_is_estimated BOOLEAN "
                "NOT NULL DEFAULT false"
            ),
        )
        await conn.execute(
            text(
                """
                DO $$
                BEGIN
                  IF EXISTS (
                    SELECT 1 FROM information_schema.columns
                    WHERE table_schema = 'public'
                      AND table_name = 'ingredient_manager'
                      AND column_name = 'quantity'
                      AND data_type IN ('double precision', 'real', 'numeric')
                  ) THEN
                    UPDATE ingredient_manager
                    SET quantity = GREATEST(1, ROUND(quantity)::integer),
                        min_quantity = GREATEST(1, ROUND(min_quantity)::integer);
                    ALTER TABLE ingredient_manager
                      ALTER COLUMN quantity TYPE INTEGER USING quantity::integer;
                    ALTER TABLE ingredient_manager
                      ALTER COLUMN min_quantity TYPE INTEGER USING min_quantity::integer;
                  END IF;
                END $$;
                """
            ),
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    await _migrate_tables()
    try:
        yield
    finally:
        await dispose_engine()


app = FastAPI(title="cloverky Main Page", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inventory_router)



@app.get("/")
def read_root():
    return {"message": "FAST API 메인 페이지 ", "docs": "/docs"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    """
    JSON 본문 `{"message": "..."}` 를 받아 Gemini 답변 문자열을 반환합니다.
    """
    if not keymaker.is_gemini_ready():
        raise HTTPException(
            status_code=503,
            detail="GEMINI_API_KEY가 설정되지 않았습니다. backend/.env 에 키를 넣어 주세요.",
        )

    model = keymaker.get_gemini_model()
    try:
        response = model.generate_content(req.message)
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Gemini 호출 실패: {e!s}",
        ) from e

    try:
        text = (response.text or "").strip()
    except ValueError as e:
        feedback = getattr(response, "prompt_feedback", None)
        raise HTTPException(
            status_code=400,
            detail=f"응답 텍스트를 읽을 수 없습니다: {e!s}. prompt_feedback={feedback}",
        ) from e

    if not text:
        reason = None
        if getattr(response, "candidates", None):
            c0 = response.candidates[0]
            reason = getattr(c0, "finish_reason", None)
        raise HTTPException(
            status_code=502,
            detail=(
                "모델이 비어 있는 응답을 반환했습니다."
                + (f" (finish_reason={reason})" if reason else "")
            ),
        )

    return ChatResponse(reply=text)


@app.get("/weather", response_model=WeatherResponse)
def get_weather(
    city: str | None = Query(None, description="도시명 (미입력 시 keymaker 기본값)"),
    country: str | None = Query(None, description="국가 코드 (예: KR)"),
) -> WeatherResponse:
    """
    OpenWeather Current Weather API — `keymaker` 의 OpenWeather 설정을 사용합니다.
    """
    if not keymaker.is_openweather_ready():
        raise HTTPException(
            status_code=503,
            detail="OPENWEATHER_API_KEY가 설정되지 않았습니다. backend/.env 에 키를 넣어 주세요.",
        )

    appid = keymaker.get_openweather_api_key()
    q_city = (city or keymaker.get_openweather_default_city()).strip()
    q_country = (country or keymaker.get_openweather_default_country()).strip()
    query = f"{q_city},{q_country}"

    params = urllib.parse.urlencode(
        {
            "q": query,
            "appid": appid,
            "units": "metric",
            "lang": "kr",
        }
    )
    url = f"https://api.openweathermap.org/data/2.5/weather?{params}"

    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise HTTPException(
            status_code=502,
            detail=f"OpenWeather 호출 실패 ({e.code}): {body}",
        ) from e
    except urllib.error.URLError as e:
        raise HTTPException(
            status_code=502,
            detail=f"OpenWeather 연결 실패: {e.reason}",
        ) from e
    except (json.JSONDecodeError, KeyError) as e:
        raise HTTPException(
            status_code=502,
            detail=f"OpenWeather 응답 파싱 실패: {e!s}",
        ) from e

    try:
        main = data["weather"][0]
        return WeatherResponse(
            city=data["name"],
            country=data["sys"]["country"],
            temp_c=float(data["main"]["temp"]),
            feels_like_c=float(data["main"]["feels_like"]),
            description=main["description"],
            icon=main["icon"],
            humidity=int(data["main"]["humidity"]),
        )
    except (KeyError, TypeError, ValueError) as e:
        raise HTTPException(
            status_code=502,
            detail=f"OpenWeather 응답 형식 오류: {e!s}",
        ) from e


@app.get("/db-check")
async def check_db(db: AsyncSession = Depends(get_db)):
    return await DbHealthAdapter.neon_time_check(db)


@app.get("/titanic/data")
def read_titanic_data():
    james = JamesController()
    df = james.get_data()

    return df.to_dict(orient="records")


@app.get("/titanic/count")
def read_titanic_count():
    james = JamesController()
    count = james.get_count()

    return {"count": count}


@app.get("/titanic/tree")
def read_titanic_tree():
    james = JamesController()
    tree = james.has_decision_tree_model()

    return {"tree": tree}


@app.get("/titanic/count/survived")
def read_titanic_count_survived():
    james = JamesController()
    count = james.get_count_survived()

    return {"count": count}


@app.get("/titanic/count/not_survived")
def read_titanic_count_not_survived():
    james = JamesController()
    count = james.get_count_not_survived()

    return {"count": count}


@app.get("/titanic/model")
def read_titanic_model():
    controller = JamesController()
    model_name = controller.get_model_name_and_accuracy()
    return JSONResponse(content=jsonable_encoder(model_name))


@app.get("/doro/data")
def read_doro_data():
    doro_director = DoroDirector()
    df = doro_director.get_data()

    return df.to_dict(orient="records")


# 회원가입 · 로그인 (Neon DB — 비밀번호 해시 저장)
@app.get("/signup/check-username", response_model=UsernameCheckResponse)
async def check_username(
    username: str = Query(..., min_length=2, max_length=20),
    db: AsyncSession = Depends(get_db),
) -> UsernameCheckResponse:
    """아이디 중복 확인 (users 테이블)."""
    u = username.strip()
    if not re.fullmatch(r"[a-zA-Z0-9_]{2,20}", u):
        return UsernameCheckResponse(
            username=u,
            available=False,
            message="아이디는 2~20자의 영문, 숫자, _ 만 사용할 수 있습니다.",
        )

    try:
        result = await asyncio.wait_for(
            db.execute(
                select(User.id).where(func.lower(User.username) == _username_key(u)).limit(1),
            ),
            timeout=8.0,
        )
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=503,
            detail="DB 응답이 지연되고 있습니다. 잠시 후 다시 시도해 주세요.",
        ) from None
    except Exception as e:
        logger.exception("check_username DB error")
        raise HTTPException(
            status_code=503,
            detail="아이디 확인 중 서버 오류가 발생했습니다.",
        ) from e

    if result.scalar_one_or_none() is not None:
        return UsernameCheckResponse(
            username=u,
            available=False,
            message="이미 사용 중인 아이디입니다.",
        )

    return UsernameCheckResponse(
        username=u,
        available=True,
        message="사용 가능한 아이디입니다.",
    )


@app.post("/signup", response_model=SignUpResponse)
async def signup(req: SignUpRequest, db: AsyncSession = Depends(get_db)) -> SignUpResponse:
    """
    회원가입 — FastAPI + Neon DB.

    필수 JSON 필드:
    - name, username, email
    - password, confirmPassword (8자 이상, 서로 일치)
    - agreeTerms: true
    """
    if not req.agree_terms:
        raise HTTPException(status_code=400, detail="약관에 동의해야 합니다.")

    if len(req.password) < 8:
        raise HTTPException(status_code=400, detail="비밀번호는 8자 이상이어야 합니다.")

    if req.password != req.confirm_password:
        raise HTTPException(status_code=400, detail="비밀번호가 일치하지 않습니다.")

    username = req.username.strip()
    email = req.email.strip()
    name = req.name.strip()

    user = await UserController().save_user(
        db,
        UserSchema(
            username=username,
            name=name,
            email=email,
            password=req.password,
            role=UserRole.USER.value,
            agree_terms=req.agree_terms,
        ),
    )

    logger.info(
        "회원가입 완료(DB) — username=%r name=%r email=%r role=%s",
        user.username,
        user.name,
        user.email,
        user.role,
    )

    return SignUpResponse(
        message=f"회원가입이 완료되었습니다. {user.username}님, 이제 로그인해 주세요.",
        username=user.username,
        email=user.email,
    )


@app.post("/login", response_model=LoginResponse)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)) -> LoginResponse:
    """로그인 — Controller → Service → Repository 레이어 로그를 남기며 인증."""
    result = await UserController().login_user(
        db,
        LoginSchema(
            email=req.email,
            password=req.password,
        ),
    )

    logger.info(
        "로그인 완료(DB) — username=%r name=%r email=%r",
        result.username,
        result.name,
        result.email,
    )

    return LoginResponse(
        message="로그인되었습니다.",
        name=result.name,
        username=result.username,
        email=result.email,
    )




if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)