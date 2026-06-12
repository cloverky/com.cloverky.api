# Backend 엔티티·테이블 규칙 (FridgeAI)

> DB 테이블·ORM 모델 작성 전 **본 문서를 읽고** 적용한다.  
> 인덱스: [`docs/DevOps/README.md`](../README.md)

---

## 1. 기본 원칙 (필수)

**이 프로젝트의 모든 테이블은 반드시 아래를 따른다.**

| 항목 | 규칙 |
|------|------|
| 기본 키(PK) 타입 | **`int`** (자동 증감) |
| 기본 키 컬럼명 | **`id`** (다른 이름 금지: `user_id`를 PK로 쓰지 않음) |
| 역할 | 시스템 내부용 고유 번호 (서로 다른 테이블 간 참조는 `xxx_id` FK 사용) |

- PK는 **한 테이블당 하나**, 이름은 항상 **`id`**.
- 다른 테이블을 가리킬 때만 `user_id`, `ingredient_id`처럼 **`{대상}_id`** FK를 둔다.

---

## 2. SQLModel로 정의할 때 (권장 템플릿)

신규 테이블·모델은 아래 패턴을 **그대로** 사용한다.

```python
from typing import Optional

from sqlmodel import Field, SQLModel


class Example(SQLModel, table=True):
    __tablename__ = "example"

    # 1. 시스템 내부용 자동 증감 고유 번호 (기본 키)
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},  # DB 컬럼명: id
    )

    # 이하 비즈니스 컬럼 …
    # user_id: int = Field(foreign_key="users.id")  # FK 예시
```

### 필드 의미

- **`Optional[int]` + `default=None`**: INSERT 시 DB가 값을 채움 (auto increment).
- **`primary_key=True`**: 기본 키.
- **`sa_column_kwargs={"name": "id"}`**: 실제 DB 컬럼명을 `id`로 고정.

---

## 3. SQLAlchemy 2.x (`Mapped`) — 현재 코드베이스

`backend/apps/models/` 등에 이미 SQLAlchemy 스타일이 있으면, **동일 규칙**으로 `id`만 맞춘다.

```python
from sqlalchemy.orm import Mapped, mapped_column

class Example(Base):
    __tablename__ = "example"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
```

### 프로젝트 공통 믹스인 (SQLAlchemy)

```python
from models.entity_id import EntityIdMixin

class User(EntityIdMixin, Base):
    __tablename__ = "users"
    # id 는 EntityIdMixin 에서 상속
```

| 파일 | 역할 |
|------|------|
| `backend/apps/models/entity_id.py` | `EntityIdMixin` — PK `id` 정의 |
| `backend/apps/main.py` → `_ensure_entity_rule_schema` | 기동 시 레거시 `secom_users` 제거, `id` 없는 테이블 보강 |

### 프로젝트 참고 구현

| 테이블 | 모델 | PK |
|--------|------|-----|
| `users` | `apps/models/user.py` → `User` | `EntityIdMixin` → `id` |
| `ingredient_manager` | `apps/models/ingredient_manager.py` → `IngredientManager` | `EntityIdMixin` → `id` |

---

## 4. 금지·주의

| ❌ 하지 말 것 | ✅ 대신 |
|-------------|--------|
| PK 이름을 `user_id`, `pk`, `uuid` 등으로 정의 | PK는 항상 **`id`** |
| PK를 UUID·문자열로 두기 (별도 승인 없이) | **`int` 자동 증감** |
| 테이블마다 PK 컬럼명을 다르게 짓기 | 전 테이블 **`id`** 통일 |
| `id` 없이 테이블 생성 | 마이그레이션·모델 추가 전 **본 규칙 확인** |

---

## 5. Cursor / Agent에 줄 지시 (복사용)

```text
이 프로젝트의 모든 테이블은 int 자동 증감 PK이며 컬럼명은 id로 통일한다.
SQLModel이면 아래 패턴을 따른다:

id: Optional[int] = Field(
    default=None,
    primary_key=True,
    sa_column_kwargs={"name": "id"},
)

docs/DevOps/Backend/ENTITY_RULE.md 를 참고해 모델·마이그레이션을 작성해 주세요.
```

---

## 6. 마이그레이션·FK

- Alembic / `main.py` `_migrate_tables()` 로 테이블을 만들 때도 PK 컬럼명은 **`id`**.
- FK는 `ForeignKey("users.id")`처럼 **참조 테이블의 `id`** 를 가리킨다.
- 인덱스가 필요하면 `user_id` 등 FK 컬럼에 `index=True` (PK `id`와 혼동하지 않기).
