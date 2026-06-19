# titanic — 앱 CLAUDE.md

> 루트 원칙: [`../../../../CLAUDE.md`](../../../../CLAUDE.md)
> 엔티티·테이블 규칙: [[ENTITY_RULE]]

---

## 개요

titanic은 타이타닉 데이터셋 기반의 ML 파이프라인 bounded context다.  
fridge와 **동일한 헥사고날 레이아웃**을 따른다. `app/domain/` 폴더는 사용하지 않는다.

앞으로 `fridge`, `secom` 처럼 **시블링 앱들이 `clover/apps/` 아래 계속 추가**될 예정이며,  
각 앱은 자신의 `_docs/CLAUDE.md`에 앱별 명세를 관리한다.

---

## 라우트 구조

모든 titanic 엔드포인트는 `/api/titanic/{name}/...` 형태다.

| 설정 위치 | 값 |
|----------|-----|
| `titanic_router` prefix | `/api/titanic` (`adapter/inbound/api/__init__.py`) |
| 각 캐릭터 라우터 prefix | `/{name}` (`adapter/inbound/api/v1/*_router.py`) |
| `main.py` 등록 | `app.include_router(titanic_router)` 단일 등록 |

> 같은 router 객체를 두 번 `include_router`하면 두 번째 등록이 무시된다. 항상 단일 등록.

---

## 캐릭터 라우터 목록

각 캐릭터는 독립된 슬라이스(router + interactor + repository + dependencies)를 가진다.

| 캐릭터 | 파일명 | 엔드포인트 | 역할 |
|--------|--------|-----------|------|
| 제임스 카메론 | `crew_james_director_router.py` | `/api/titanic/james/...` | CSV 업로드, 데이터 적재 총괄 |
| 월터 | `crew_walter_roaster_router.py` | `/api/titanic/walter/...` | 승객 명단 관리 |
| 토마스 앤드류스 | `crew_andrews_architect_router.py` | `/api/titanic/andrews/...` | 시스템 구조·메타데이터 |
| 왈리스 하틀리 | `crew_hartley_violin_router.py` | `/api/titanic/hartley/...` | 배경 작업·이벤트 스트리밍 |
| 해롤드 로우 | `crew_Iowe_boat_router.py` | `/api/titanic/lowe/...` | 구조 작업 |
| 스미스 선장 | `crew_smith_captain_router.py` | `/api/titanic/smith/...` | 전체 승객 현황·통계 |
| 칼 하클리 | `passenger_cal_tester_router.py` | `/api/titanic/cal/...` | 입력값 유효성 검사 |
| 이시도르 부부 | `passenger_isidor_couple_router.py` | `/api/titanic/isidor/...` | 커플 데이터 처리 |
| 잭 도슨 | `passenger_jack_trainer_router.py` | `/api/titanic/jack/...` | 생존 예측 모델 인터페이스 |
| 몰리 브라운 | `passenger_molly_scaler_router.py` | `/api/titanic/molly/...` | 피처 스케일링 |
| 로즈 | `passenger_rose_model_router.py` | `/api/titanic/rose/...` | 예측 모델 |
| 루스 | `passenger_ruth_survivor_router.py` | `/api/titanic/ruth/...` | 1등석 승객(상류층) 조회 |

---

## 슬라이스 폴더 구조

```
titanic/
├── adapter/
│   ├── inbound/api/
│   │   ├── __init__.py          # titanic_router 조립 (prefix="/api/titanic")
│   │   ├── schemas/             # Pydantic 요청·응답 스키마
│   │   └── v1/                  # *_router.py (prefix="/{name}")
│   └── outbound/
│       ├── orm/                 # *_orm.py
│       └── pg/                  # *PgRepository
├── app/
│   ├── dtos/
│   ├── ports/
│   │   ├── input/               # *UseCase ABC
│   │   └── output/              # *Repository ABC
│   └── use_cases/               # *Interactor
├── dependencies/                # get_*_use_case 팩토리
└── _docs/
    └── CLAUDE.md                # 이 파일
```

---

## 새 캐릭터(슬라이스) 추가 순서

1. `app/dtos/` — DTO
2. `app/ports/input/` — `*UseCase` ABC
3. `app/ports/output/` — `*Repository` ABC
4. `app/use_cases/` — `*Interactor`
5. `adapter/outbound/orm/` — ORM
6. `adapter/outbound/pg/` — `*PgRepository`
7. `adapter/inbound/api/schemas/` — Pydantic 스키마
8. `adapter/inbound/api/v1/` — `*_router.py` (prefix=`/{name}`)
9. `dependencies/` — `get_*_use_case`
10. `adapter/inbound/api/__init__.py`의 `_routers` 리스트에 추가

---

## 자주 하는 실수

| 실수 | 올바른 방향 |
|------|------------|
| 라우터 prefix에 `/api/titanic/` 직접 기입 | prefix=`/{name}` 만 — 부모 router가 `/api/titanic` 담당 |
| `titanic_router`를 `main.py`에서 두 번 등록 | 단일 `app.include_router(titanic_router)` |
| provider 함수명과 router import명 불일치 | `get_*_use_case` 명명 규칙 통일 |
| `app/domain/` 생성 | `app/use_cases/_*.py` 사용 |

## async def vs def 판단 기준

UseCase / Port 메소드에 `async`를 붙일지 말지는 **I/O 여부**로 결정한다.

| 성격 | 형태 | 예시 |
|------|------|------|
| I/O-bound (DB, LLM, HTTP) | `async def` | `introduce_myself`, `receive_uploaded_records` |
| CPU-bound (형태소 분석, 순수 연산) | `def` | `analyze_intent` (Kiwi) |

`async def`는 코루틴을 만들 뿐, CPU 연산을 비블로킹으로 바꿔주지 않는다.
Kiwi 같은 CPU 작업에 `async def`를 붙이면 이벤트 루프를 막으면서 비블로킹처럼 보이는 함수가 돼 더 나쁘다.

Kiwi 처리가 무거워 이벤트 루프 블로킹이 실제 문제가 된다면, 포트 시그니처는 `def`로 유지하고 **호출 측**에서 스레드풀로 오프로드한다:

```python
result = await asyncio.to_thread(use_case.analyze_intent, question)
```

---

## 타이타닉 도메인 문서 연결

- 타이타닉 도메인 문서 연결
- 타이타닉 피처 정리[[titanic-features]]
- 타이타닉 머신러닝[[titanic-machine-learning]]
- 타이타닉 ERD[[titanic-erd]]
- 타이타닉 nf[[titanic-nf]]
- 타이타닉 알고리즘[[titanic-algorithm]]