# clover — 백엔드 CLAUDE.md

> 루트 원칙: `../CLAUDE.md` 를 먼저 읽는다.

---

## 저장소 개요

| 항목 | 내용 |
|------|------|
| 형태 | 모노레포 (`clover/` 백엔드 + `lucky/` 프론트엔드) |
| 백엔드 진입점 | `clover/main.py` (FastAPI) |
| 앱 패키지 위치 | `clover/apps/` (`fridge`, `titanic`, `secom`, `matrix` 등) |
| `sys.path` | `main.py`가 `clover/`·`clover/apps/`를 삽입 — import는 `fridge.*`, `titanic.*` 형태 |
| DB | Neon PostgreSQL, SQLAlchemy 2.x async (`psycopg`) |
| 배포 | Docker Compose (`docker-compose.yaml`) — 코드 변경 후 `docker compose build backend && docker compose up -d backend` |

---

## 모듈 경로 규칙

| 범위 | 규칙 | 예시 |
|------|------|------|
| **앱 / bounded context** | `clover`·`apps` 없이 시작 | `fridge/adapter/inbound/...`, import `fridge.app.use_cases...` |
| **공유 코어** | `clover.core.` 접두사 | `clover.core.database`, `clover.core.matrix.oracle_database` |
| **금지** | `clover.apps.fridge`, `apps.fridge` 등 중복 접두사 | — |

다른 에이전트에 파일 위치를 안내할 때: `fridge/dependencies/inventory.py` (not `clover/apps/fridge/...`).

---

## 헥사고날 아키텍처 (Ports & Adapters)

도메인 앱(`fridge`, `titanic`)은 **헥사고날**을 기준으로 폴더를 나눈다.

```
{app}/
├── adapter/
│   ├── inbound/          # 외부 → 앱 (HTTP API, Pydantic schema)
│   └── outbound/         # 앱 → 외부 (DB, 외부 API, 파일)
│       ├── orm/          # SQLAlchemy 엔티티
│       ├── pg/           # Repository 구현체 (*PgRepository)
│       └── gemini/       # (fridge) 외부 AI 연동
├── app/
│   ├── dtos/             # 유스케이스 입출력 데이터
│   ├── ports/
│   │   ├── input/        # 인바운드 포트 (UseCase ABC)
│   │   └── output/       # 아웃바운드 포트 (Repository ABC)
│   └── use_cases/        # Interactor — 비즈니스 로직
├── dependencies/         # DIP 팩토리 (FastAPI Depends 조립)
└── models/
    └── database.py       # (fridge만) DB compat re-export — 옮기지 말 것
```

**`domain/` 폴더는 사용하지 않는다.** 순수 보조 로직은 `app/use_cases/_*.py` (예: `_shelf_life.py`)에 둔다.

---

## 클린 아키텍처 레이어 대응

| 클린 레이어 | 이 프로젝트 위치 |
|------------|-----------------|
| Entities / Domain rules | `app/use_cases/_*.py`, interactor 내부 순수 함수 |
| Use Cases | `app/use_cases/*_interactor.py` |
| Interface Adapters | `adapter/inbound`, `adapter/outbound` |
| Frameworks & Drivers | FastAPI, SQLAlchemy, Gemini SDK |
| DI / Composition Root | `dependencies/*.py`, `main.py` |

**의존 방향 (안쪽으로만):**

```
adapter/inbound  →  app/ports/input, app/dtos
adapter/outbound →  app/ports/output, app/dtos
app/use_cases    →  app/ports/*, app/dtos, app/use_cases/_*
dependencies     →  adapter/outbound, app/use_cases, app/ports
```

- `adapter`는 `app/ports`의 **인터페이스**만 안다.
- `use_cases`는 `adapter` 구현체를 **직접 import하지 않는다**.
- 구현체 조립은 **`dependencies/`** 에서만 한다.

---

## SOLID 적용

| 원칙 | 적용 방식 |
|------|----------|
| **SRP** | 라우터=HTTP 위임, Interactor=비즈니스, PgRepository=영속화, ORM=테이블 매핑 각각 분리 |
| **OCP** | 새 저장소·외부 연동은 `ports/output` ABC + `adapter/outbound` 구현 추가 |
| **LSP** | `InventoryUseCase` 등 포트 타입으로 주입; 구현체 교체 가능 |
| **ISP** | 슬라이스별 UseCase·Repository 분리 (`inventory`, `food_catalog`, `receipt_scan` …) |
| **DIP** | `dependencies/get_*_use_case`가 구현체를 조립하고 **포트 타입**으로 반환 |

---

## 주요 디자인 패턴

| 패턴 | 위치 | 역할 |
|------|------|------|
| **Port (Interface)** | `app/ports/input`, `app/ports/output` | ABC로 계약 정의 |
| **Interactor (Use Case)** | `app/use_cases/*_interactor.py` | 포트 구현 + 오케스트레이션 |
| **Repository** | `*PgRepository` | `ports/output` 구현, ORM↔DTO 변환 |
| **DTO** | `app/dtos/` | 레이어 간 데이터 (ORM/Pydantic과 분리) |
| **Adapter** | `adapter/inbound/api/schemas` | HTTP 요청/응답 Pydantic + `mappers.py` |
| **Factory / Composition Root** | `dependencies/*.py` | `Depends(get_db)` + Repository + Interactor 조립 |
| **Thin Controller** | `adapter/inbound/api/v1/*_router.py` | 파싱·위임·응답 매핑만 |

---

## FastAPI 규칙

### 라우터 (Thin Delegation)

라우터는 **얇게** 유지한다. 비즈니스 로직·DB 접근 금지.

```python
# ✅ 올바른 패턴
@inventory_router.get("")
async def list_inventory(
    x_user_email: str = Header(..., alias="X-User-Email"),
    inventory: InventoryUseCase = Depends(get_inventory_use_case),
) -> InventoryListResponse:
    return to_inventory_list_response(await inventory.list_inventory(x_user_email))
```

- `Depends` 인자 타입: **구현체가 아닌 포트** (`InventoryUseCase`, `JamesDirectorUseCase`)
- 팩토리: `dependencies/` 모듈의 `get_*_use_case`
- HTTP 스키마: `adapter/inbound/api/schemas/`
- DTO ↔ Response 변환: `schemas/mappers.py`

### 라우터 조립

- **fridge**: `adapter/inbound/api/fridge_router.py` — `__init__.py`에 로직 넣지 않음
- **titanic**: `adapter/inbound/api/__init__.py`에 `titanic_router` 조립 (titanic만 예외)
- `main.py`: `app.include_router(fridge_router)`, `app.include_router(titanic_router)`

### 슬라이스별 API (fridge)

| 슬라이스 | prefix | UseCase | dependencies |
|---------|--------|---------|--------------|
| inventory | `/inventory` | `InventoryInteractor` | `dependencies/inventory.py` |
| food catalog | `/foods` | `FoodCatalogInteractor` | `dependencies/food_catalog.py` |
| category catalog | `/categories` | `CategoryCatalogInteractor` | `dependencies/category_catalog.py` |
| receipt scan | `/receipts` | `ReceiptScanInteractor` | `dependencies/receipt_scan.py` |

---

## DIP 팩토리 템플릿

`dependencies/` 모듈은 **유일한 조립 지점**이다.

```python
def get_inventory_use_case(
    db: AsyncSession = Depends(get_db),
) -> InventoryUseCase:
    users: UserRepository = UserPgRepository(session=db)
    inventory: InventoryRepository = InventoryPgRepository(session=db)
    return InventoryInteractor(users=users, inventory=inventory, ...)
```

규칙:

- `get_db`는 **`core.matrix.oracle_database`** 에서 import (단일 소스)
- 지역 변수 타입 힌트: **포트(ABC)** 로 선언
- 반환 타입: **input 포트** (`*UseCase`)
- 라우터·Interactor는 `*PgRepository`를 **직접 import하지 않음**

---

## 새 기능 추가 체크리스트

슬라이스 하나를 추가할 때 (titanic·fridge 공통):

1. `app/dtos/` — Command/Result DTO
2. `app/ports/input/` — `*UseCase` ABC
3. `app/ports/output/` — `*Repository` ABC (필요 시)
4. `app/use_cases/` — `*Interactor`
5. `adapter/outbound/orm/` — ORM (테이블 있을 때)
6. `adapter/outbound/pg/` — `*PgRepository`
7. `adapter/inbound/api/schemas/` — Request/Response Pydantic
8. `adapter/inbound/api/v1/` — `*_router.py`
9. `dependencies/` — `get_*_use_case`
10. 상위 라우터에 `include_router`
11. `main.py` / `alembic/env.py`에 ORM `# noqa: F401` import (create_all·autogenerate)

검증: `cd clover && python -c "import main"`

---

## `__init__.py` 규칙

**fridge의 모든 `__init__.py`는 비어 있어야 한다** (0바이트).

- 패키지 마커 역할만
- re-export·라우터 조립·`__all__` 정의 금지
- 조립 로직은 `fridge_router.py` 같은 **명명된 모듈**에 둔다

(titanic은 `adapter/inbound/api/__init__.py`에 `titanic_router` 조립이 남아 있음 — fridge와의 차이점)

---

## DB·ORM 규칙

### 옮기지 말 것

| 경로 | 역할 |
|------|------|
| `clover/apps/database.py` | 실제 `Base`, engine, `get_db` 구현 (→ `core/database.py` re-export) |
| `clover/apps/fridge/models/database.py` | `from database import …` compat — Alembic·레거시 import 유지 |

### Neon 테이블명 (fridge)

접두사 `fridge_` **없음**:

| 테이블 | 용도 |
|--------|------|
| `users` | 회원 (`default_storage` 컬럼) |
| `categories` | 식품 카테고리 |
| `foods` | 식품 마스터 |
| `inventory` | 회원별 재고 (`food_id` FK) |
| `receipts`, `receipt_lines` | 영수증 스캔 |

**삭제된 레거시:** `ingredient_manager`, `inventory_items`, `fridge_*` 접두사 테이블 — `main.py` `_drop_legacy_fridge_tables`에서 DROP.

### ORM 규칙

- 위치: `adapter/outbound/orm/*_orm.py`
- `from database import Base` (titanic·fridge 동일)
- fridge 엔티티: `EntityIdMixin` + `*Orm` 클래스명 (`InventoryOrm` 등)
- ORM은 DTO/스키마로 변환하지 않고 **Repository**에서 DTO로 매핑

### DB 세션

- 앱 코드: `from core.matrix.oracle_database import get_db`
- `main.py` lifespan: `fridge.models.database`의 `engine`, `Base.metadata.create_all`
- Alembic: `fridge.models.database.Base` + ORM F401 import

---

## fridge 도메인 결정 사항

### `inventory` + `foods` 통합 (A안 확정)

- 회원 재고는 `inventory` 테이블 + `foods` 마스터 조인
- `ingredient_manager` 단일 테이블 방식 **폐기** (모델·마이그레이션·API 모두 제거)
- `InventoryInteractor`가 `FoodRepository`로 `food_id` resolve/create

### 보조 로직 `_shelf_life.py`

유통기한 추정·재고 상태(`양호`/`임박`/`긴급`/`부족`) 순수 함수.

- 위치: `app/use_cases/_shelf_life.py`
- 사용처: `inventory_interactor`, `receipt_scan_interactor`, `schemas/mappers.py`

### 삭제된 레거시 (재도입 금지)

```
fridge/controllers/
fridge/services/
fridge/repositories/
fridge/schemas/          # → adapter/inbound/api/schemas/
fridge/domain/           # → use_cases/_shelf_life.py
fridge/models/category.py 등 re-export
models/ingredient_manager.py
```

---

## secom (레거시 MVC)

`clover/apps/secom`은 **아직 MVC** (`controllers`, `services`, `repositories`).

| 항목 | 내용 |
|------|------|
| 인증 | `secom/app/utils/auth_password.py` (hash/verify) — **fridge에 두지 않음** |
| 회원 ORM | `models/user.py` (`users` 테이블) |
| fridge 연동 | 재고 API는 `X-User-Email` 헤더로 사용자 식별 |

secom을 fridge/titanic 구조로 옮기는 작업은 **별도 요청 시** 진행. 임의로 섞지 않는다.

---

## 자주 하는 실수 (하지 말 것)

| 실수 | 올바른 방향 |
|------|------------|
| `app/domain/` 또는 `fridge/domain/` 생성 | `app/use_cases/_*.py` 사용 |
| `__init__.py`에 라우터·re-export | 명명된 `.py` 모듈로 분리 |
| 라우터에서 `PgRepository` 직접 사용 | `Depends(get_*_use_case)` + 포트 타입 |
| Interactor에서 ORM import | Repository 포트만 의존 |
| `fridge_users`, `fridge_inventory` 테이블명 | `users`, `inventory` |
| `database.py` / `fridge/models/database.py` 이동 | 경로 고정 |
| `ingredient_manager` 재도입 | A안 `inventory`+`foods` 유지 |
| fridge 비밀번호 로직을 fridge에 둠 | `secom/app/utils/auth_password.py` |
| 요청 없는 리팩터·포맷 변경 | 루트 §3 Surgical Changes |

---

## 요청 흐름 (fridge inventory 예시)

```
Client
  → inventory_router          [adapter/inbound]
      Depends(InventoryUseCase)
  → get_inventory_use_case    [dependencies — DIP]
      InventoryPgRepository + InventoryInteractor 조립
  → InventoryInteractor       [app/use_cases]
      InventoryRepository, FoodRepository 포트 호출
      _shelf_life 순수 함수
  → InventoryPgRepository     [adapter/outbound/pg]
      InventoryOrm + FoodOrm  [adapter/outbound/orm]
  → mappers.to_*_response     [adapter/inbound/schemas]
  → JSON Response
```

---

## 검증·기동

```bash
# 로컬 import 확인
cd clover && python -c "import main"

# Docker 재빌드 (코드 변경 후 필수)
docker compose build backend && docker compose up -d backend
```

- fridge 라우트 수: `fridge_router` 기준 13개
- import 오류 시 `sys.path`·`apps/` 패키지명 확인
- DB 마이그레이션: `main.py` lifespan `_migrate_tables` (Neon 연결 필요)
