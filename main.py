import asyncio
import logging
import re
import selectors
import sys
from pathlib import Path

# matrix, fridge, titanic 등 앱 패키지는 backend/apps 아래에 있음
_BACKEND_ROOT = Path(__file__).resolve().parent
_APPS_DIR = _BACKEND_ROOT / "apps"
_PROJECT_ROOT = (
    _BACKEND_ROOT.parent
)  # clover.apps.* / clover.core.* 절대경로 import 지원
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))
if str(_APPS_DIR) not in sys.path:
    sys.path.insert(0, str(_APPS_DIR))

# Windows: psycopg async + uvicorn 시 DB 요청이 멈추는 문제 방지
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
import os
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Form, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from messenger.adapter.inbound.api import messenger_router
from pydantic import BaseModel, ConfigDict, Field, field_validator
from silicon_valley.adapter.inbound.api import silicon_valley_router
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.sessions import SessionMiddleware
from users.adapter.user import User, UserRole  # noqa: F401 — create_all 에 테이블 등록
from users.db_health_adapter import DbHealthAdapter
from weather_provider import fetch_seoul_weather

from core.admin_auth import SESSION_SECRET, check_credentials, get_login_html
from core.matrix.wault_keymaker_serect_manager import get_keymaker
from fridge.adapter.inbound.api.fridge_router import fridge_router
from fridge.adapter.outbound.orm.category_orm import CategoryOrm  # noqa: F401
from fridge.adapter.outbound.orm.foods_orm import FoodsOrm  # noqa: F401
from fridge.adapter.outbound.orm.inventory_orm import InventoryOrm  # noqa: F401
from fridge.adapter.outbound.orm.receipt_line_orm import ReceiptLineOrm  # noqa: F401
from fridge.adapter.outbound.orm.receipt_orm import ReceiptOrm  # noqa: F401
from fridge.models.database import Base, dispose_engine, engine, get_db
from secom.app.controllers.user_controller import UserController
from secom.app.schemas.user_schema import LoginSchema, UserSchema
from titanic.adapter.inbound.api import titanic_router
from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import (
    JackTrainerOrm,  # noqa: F401
)
from titanic.adapter.outbound.orm.passenger_rose_model_strategies_orm import (
    BookingOrm,  # noqa: F401
)
from messenger.adapter.outbound.orm.juso_orm import ContactOrm  # noqa: F401
from messenger.adapter.outbound.orm.mail_orm import MailInboxOrm  # noqa: F401
from messenger.adapter.outbound.orm.push_orm import PushSubscriptionOrm  # noqa: F401
from messenger.adapter.inbound.api.v1.push_router import push_router

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


async def _drop_legacy_fridge_tables(conn) -> None:
    """fridge_*·구 테이블 제거 후 ORM(create_all)으로 재생성. alembic_version·users 는 유지."""
    for tbl in (
        "fridge_inventory",
        "fridge_codes",
        "fridge_foods",
        "fridge_categories",
        "fridge_users",
        "ingredient_manager",
        "inventory_items",
        "codes",
    ):
        await conn.execute(text(f'DROP TABLE IF EXISTS "{tbl}" CASCADE'))


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
                'categories',
                'foods',
                'receipts',
                'receipt_lines',
                'inventory'
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
    """users·fridge 도메인 테이블 생성 및 ENTITY_RULE·스키마 보강."""
    async with engine.begin() as conn:
        await _drop_legacy_fridge_tables(conn)
        await conn.run_sync(Base.metadata.create_all)
        await _ensure_entity_rule_schema(conn)
        await conn.execute(
            text(
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(20) "
                "NOT NULL DEFAULT 'user'"
            ),
        )
        await conn.execute(
            text(
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS default_storage VARCHAR(20) "
                "NOT NULL DEFAULT '냉장'"
            ),
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("DB 마이그레이션 시작…")
    try:
        await asyncio.wait_for(_migrate_tables(), timeout=45.0)
    except TimeoutError:
        logger.error(
            "DB 마이그레이션 시간 초과(45s). DATABASE_URL·Neon 연결을 확인하세요."
        )
        raise
    except Exception:
        logger.exception("DB 마이그레이션 실패")
        raise
    logger.info("DB 마이그레이션 완료 — 서버 준비됨")
    try:
        yield
    finally:
        await dispose_engine()


app = FastAPI(
    title="cloverky Main Page",
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)


@app.get("/login", include_in_schema=False, response_model=None)
async def login_page(request: Request):
    if request.session.get("authenticated"):
        return RedirectResponse(url="/docs")
    return HTMLResponse(content=get_login_html())


@app.post("/login", include_in_schema=False, response_model=None)
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    if check_credentials(username, password):
        request.session["authenticated"] = True
        return RedirectResponse(url="/docs", status_code=303)
    return HTMLResponse(content=get_login_html(error=True), status_code=401)


@app.get("/logout", include_in_schema=False, response_model=None)
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login")


@app.get("/docs", include_in_schema=False, response_model=None)
async def custom_docs(request: Request):
    if not request.session.get("authenticated"):
        return RedirectResponse(url="/login")
    return get_swagger_ui_html(openapi_url="/openapi.json", title="cloverky API")


@app.get("/openapi.json", include_in_schema=False, response_model=None)
async def custom_openapi(request: Request):
    if not request.session.get("authenticated"):
        return JSONResponse({"detail": "Not authenticated"}, status_code=401)
    return JSONResponse(app.openapi())


app.include_router(fridge_router)
app.include_router(titanic_router)
app.include_router(silicon_valley_router)
app.include_router(messenger_router)
app.include_router(push_router, prefix="/messenger")


@app.get("/", include_in_schema=False, response_model=None)
async def read_root(request: Request):
    request.session.clear()
    return HTMLResponse(content=get_login_html())


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    """
    JSON 본문 `{"message": "..."}` 를 받아 Gemini 답변 문자열을 반환합니다.
    """
    logger.info("채팅 수신: %r", req.message)
    if not keymaker.is_gemini_ready():
        raise HTTPException(
            status_code=503,
            detail="GEMINI_API_KEY가 설정되지 않았습니다. backend/.env 에 키를 넣어 주세요.",
        )

    client = keymaker.get_gemini_client()
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=req.message,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Gemini 호출 실패: {e!s}") from e

    text = (response.text or "").strip()
    if not text:
        raise HTTPException(
            status_code=502, detail="모델이 비어 있는 응답을 반환했습니다."
        )

    return ChatResponse(reply=text)


@app.get("/weather", response_model=WeatherResponse)
def get_weather(
    city: str | None = Query(None, description="도시명 (미입력 시 keymaker 기본값)"),
    country: str | None = Query(None, description="국가 코드 (예: KR)"),
) -> WeatherResponse:
    """
    서울(또는 지정 도시) 날씨. OpenWeather 우선, 실패 시 Open-Meteo·기본값으로 항상 200 응답.
    """
    appid = (
        keymaker.get_openweather_api_key() if keymaker.is_openweather_ready() else None
    )
    q_city = (city or keymaker.get_openweather_default_city()).strip()
    q_country = (country or keymaker.get_openweather_default_country()).strip()
    payload = fetch_seoul_weather(
        openweather_appid=appid,
        city=q_city,
        country=q_country,
    )
    return WeatherResponse(**payload)


@app.get("/db-check")
async def check_db(db: AsyncSession = Depends(get_db)):
    return await DbHealthAdapter.neon_time_check(db)


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
                select(User.id)
                .where(func.lower(User.username) == _username_key(u))
                .limit(1),
            ),
            timeout=8.0,
        )
    except TimeoutError:
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
async def signup(
    req: SignUpRequest, db: AsyncSession = Depends(get_db)
) -> SignUpResponse:
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
    import os

    import uvicorn

    # Windows reload 자식 프로세스 오류 방지: 기본은 reload 끔. 필요 시 set UVICORN_RELOAD=1
    reload = (
        os.getenv("UVICORN_RELOAD", "0" if sys.platform.startswith("win") else "1")
        == "1"
    )
    logger.info("uvicorn 시작 — reload=%s http://127.0.0.1:8000", reload)
    host = "127.0.0.1"
    port = int(os.getenv("PORT", "8000"))

    if sys.platform.startswith("win") and not reload:
        loop = asyncio.SelectorEventLoop(selectors.SelectSelector())
        asyncio.set_event_loop(loop)
        config = uvicorn.Config(app, host=host, port=port, loop="asyncio")
        server = uvicorn.Server(config)
        loop.run_until_complete(server.serve())
    else:
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=reload,
            loop="asyncio",
        )
