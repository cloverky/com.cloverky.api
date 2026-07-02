# [Specification] Watson Watcher Hub — 정책 기반 필터링 및 트리아지 명세

## 1. 시스템 개요 및 아키텍처 맥락

본 시스템은 허브 앤 스포크(Hub-and-Spoke) 및 온톨로지 기반의 멀티 에이전트 아키텍처이며,
인바운드 게이트웨이 단계에서 정책 기반 비속어/욕설 필터링(KcELECTRA)을 통합한 트리아지 환경을 정의한다.

| 구분 | 역할 | 실제 경로 |
|------|------|-----------|
| **Hub / Brain** | 최고 오케스트레이터 (EXAONE) | `core/lol/t1_mid_faker_orchestrator.py` |
| **Ontology Hub** | 전사 데이터 흐름 및 온톨로지 총괄 | `apps/star_craft/` |
| **Communication Spoke** | 외부 채널 인바운드 전담 | `apps/messenger/` |
| **Triage Nurse (Watson)** | 정책 필터링 + 1차 의도 분류 게이트웨이 | `apps/messenger/adapter/inbound/api/v1/watcher_router.py` |

---

## 2. 에이전트 핵심 로직 및 라우팅 기준

외부 채널(`telegram_router`, `discord_router`, `receive_router`)로 수신된 모든 인바운드 이벤트는 Watson 게이트웨이에서 아래 3단계 정책에 따라 검증 및 라우팅된다.

### [Step 1] 정책 필터링 — 비속어/욕설 차단

- **적용 모델**: `beomi/KcELECTRA-base` (구어체·자음 조합 악성 발언 탐지 특화)
- **동작**: 인입 텍스트를 분석하여 정책 위반 여부 판단
- **위반 감지 시**: 이후 모든 라우팅을 즉각 중단 → 이벤트 폐기(Drop) → 보안 로그 기록
- **통과 시**: Step 2로 진행

### [Step 2] 일반 업무 분류 (Case A — Holmes)

- **조건**: Step 1 통과 + 중요 거래처 아님 (`important_client: false`) 또는 단순 문의
- **결과**: `messenger/app/use_cases/` 인터랙터가 자체 처리 및 종결
- **routing 값**: `"holmes"`

### [Step 3] 에스컬레이션 업무 분류 (Case B — Faker)

- **조건**: Step 1 통과 + `important_client: true` + 보고서/실적 요청 의도 감지
- **에스컬레이션 키워드**: `"보고서"`, `"실적"`, `"에스컬레이션"`, `"report"`, `"escalat"`
- **결과**: `apps/star_craft/app/use_cases/mail_orchestrator.py` 경유 → `core/lol/t1_mid_faker_orchestrator.py` 최종 활성화
- **routing 값**: `"faker"`

---

## 3. 구현 파일 맵

| 레이어 | 파일 경로 |
|--------|-----------|
| 인바운드 라우터 | `messenger/adapter/inbound/api/v1/watcher_router.py` |
| 스키마 | `messenger/adapter/inbound/api/schemas/watcher_schema.py` |
| UseCase 포트 | `messenger/app/ports/input/watcher_use_case.py` |
| DTO | `messenger/app/dtos/watcher_dto.py` |
| 인터랙터 (트리아지 + 필터링 로직) | `messenger/app/use_cases/watcher_interactor.py` |
| DI 팩토리 | `messenger/dependencies/watcher_provider.py` |
| 온톨로지 버스 (에스컬레이션 대상) | `apps/star_craft/app/use_cases/mail_orchestrator.py` |
| 최고 오케스트레이터 | `core/lol/t1_mid_faker_orchestrator.py` |

---

## 4. 테스트 시나리오

| # | 발신자 | 메시지 특성 | Step 1 결과 | 최종 라우팅 |
|---|--------|------------|-------------|------------|
| Scenario A | 일반 거래처 | 단순 인사/문의 | 통과 | `holmes` — 내부 처리 |
| Scenario B | 중요 거래처 | 비속어·욕설 포함 보고서 요청 | **차단** | 폐기 + 보안 로그 |
| Scenario C | VIP 거래처 | 정상 "분기 실적 보고서 요청" | 통과 | `faker` — 에스컬레이션 |

---

## 5. Docker 인프라 요구사항

- **Base Image**: `python:3.10-slim` 계열 경량 이미지
- **의존성**: `torch`, `transformers` (KcELECTRA 추론용)
- **환경 변수**: `PYTHONUNBUFFERED=1` (실시간 콘솔 출력)
- **실행 구조**: 컨테이너 기동 즉시 테스트 하네스 실행 → 이벤트 인입부터 최종 에이전트 도달까지 전체 저니를 서사 로그(Narrative Log) 형태로 콘솔 출력
