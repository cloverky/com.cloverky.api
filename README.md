# com.ragwatson

> FastAPI · Pandas · scikit-learn 기반 학습 모노레포.
> **"아고라(고대 그리스 광장)"** 를 작명 메타포로 삼아, 각 실습 모듈이 하나의 부스처럼 모여 있는 구조다.

---

## 프로젝트 개요

본 저장소는 **단일 배포용 애플리케이션이 아니라 여러 학습 실습이 공존하는 모노레포**다. 각 하위 패키지는 독립적으로 실행 가능한 FastAPI 앱 또는 학습 스켈레톤이다.

핵심 가치는 *결과물*보다 **하네스(harness) 구축 자체**다 — 데이터 적재기(Reader), 서비스(Service), 컨트롤러(Controller), 모델(Model), 검증기(Validation)로 책임을 쪼개 LLM·사람 모두 검토하기 쉬운 형태를 연습한다. 본 저장소의 AI 협업 사상은 [`CURSOR.md`](./CURSOR.md) 참조.

---

## 디렉터리 구조

```
com.ragwatson/
├── agora/                          # 모노레포 루트 (그리스 아고라 메타포)
│   ├── app/                        # 철학자 스켈레톤 — 학습용 빈 클래스
│   │   ├── socrates.py             # 질문을 던지는 자
│   │   ├── plato.py
│   │   ├── pericles.py
│   │   ├── zeno_of_citium.py
│   │   └── demosthenes.py
│   └── titanic/                    # Titanic 생존 예측 (FastAPI + Decision Tree)
│       └── app/
│           ├── james_controller.py # 컨트롤러 ("제임스가 메인이다")
│           ├── jack_service.py     # 서비스: 학습 모델 메타정보
│           ├── rose_model.py       # 모델 로더 (joblib)
│           └── caledon_validation.py
├── docs/                           # Obsidian vault (강의 메모 + 프로젝트 정리)
├── www/                            # (예약)
├── CURSOR.md                       # AI 협업 사상 (Why)
├── .cursorrules                    # AI 운영 규약 (How)
├── CLAUDE.md                       # 코드 위생 (What not)
└── README.md                       # 본 파일
```

---

## 작명 컨벤션

> 클래스/파일 이름이 인물 이름이다. 역할 → 인물의 1:1 매핑을 외우면 코드가 쉬워진다.

### 아고라 (`agora/app/`) — 그리스 철학자

| 인물 | 역할(예정) |
|---|---|
| Socrates | 질문자 — 입력/검증의 출발점 |
| Plato | 이상의 설계자 — 도메인 정의 |
| Pericles | 정치가/조정자 |
| Zeno of Citium | 스토아학파의 시조 |
| Demosthenes | 웅변가 — 외부 전달/표현 |

*현재는 모두 빈 스켈레톤이며 docstring으로 인물 설명만 보유한다.*

### 타이타닉 (`agora/titanic/app/`) — 영화 *Titanic* 캐릭터

| 인물 | 역할 |
|---|---|
| James (James Cameron) | **Controller** — API 엔드포인트 진입점 |
| Jack | **Service** — 비즈니스 로직, 모델 메타 조회 |
| Rose | **Model** — 학습된 의사결정 트리 (joblib) 로더 |
| Caledon (Cal Hockley) | **Validation** — 입력 검증 (예정) |

키 프레이즈: **"제임스가 메인이다."** (컨트롤러 = 진입점)

---

## 기술 스택

확인된 사용 기술 (코드에서 직접 import 됨):

- **Python 3.13** *(.pyc 캐시 기준 추정)*
- **FastAPI** — 웹 프레임워크
- **Uvicorn** — ASGI 서버
- **joblib** — 학습 모델 직렬화/로드
- **scikit-learn** — Decision Tree *(joblib 모델 파일 기준 추정, 직접 import는 없음)*

> 의존성은 `requirements.txt` 기준으로 설치한다.

---

## 셋업

### 1. 가상환경 생성

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. 의존성 설치

```powershell
pip install -r requirements.txt
```

> 자세한 셋업 절차는 [`docs/수업 메모/FastAPI + Unicorn 설치 & 실행.md`](./docs/수업%20메모/FastAPI%20%2B%20Unicorn%20%EC%84%A4%EC%B9%98%20%26%20%EC%8B%A4%ED%96%89.md) 참조.

---

## 실행

### Titanic API

```powershell
cd agora
python -m uvicorn titanic.app.james_controller:app --reload --host 127.0.0.1 --port 8000
```

확인:
- http://127.0.0.1:8000/docs — 자동 생성된 Swagger UI

---

## 데이터셋

프로젝트 내부 CSV 파일을 서버가 직접 읽는 구조는 제거되었다. Titanic 실습 데이터는 프론트엔드 `/lesson` 화면에서 사용자가 업로드한다.

---

## AI 협업 규약

본 저장소는 AI 에이전트(Cursor 등) 협업을 전제로 한다. **세 파일이 하나의 하네스를 구성**한다.

| 파일 | 추상 수준 | 무엇을 담는가 |
|---|---|---|
| [`CURSOR.md`](./CURSOR.md) | Why | 협업의 사상·원칙 (변하지 않음) |
| [`.cursorrules`](./.cursorrules) | How | 에이전트 운영 규약 (매 작업) |
| [`CLAUDE.md`](./CLAUDE.md) | What not | 코드 수준 위생 (diff 제약) |

충돌 시 우선순위: **`CURSOR.md` > `.cursorrules` > `CLAUDE.md`** (사상 > 규약 > 위생).
새로운 기여자(사람이든 AI든)는 작업 전에 위 세 파일을 1회 통독하라.

---

## 알려진 이슈 (현재 상태의 솔직한 보고)

> 본 README는 코드 읽기를 통해 작성됐다. 다음 사항들은 **확인된 문제**이며 본 PR 범위가 아니어서 *수정하지 않고 보고만* 한다.

1. **`agora/app/*.py` 들여쓰기 오류** — `class X:` 다음 줄의 docstring이 외곽 들여쓰기로 작성되어 있어 실행 시 `IndentationError`가 발생한다. (예: `socrates.py:3`, `plato.py:3` 등 5개 파일 전부)
2. **`agora/doro/app/_init__.py`** — 파일명 언더스코어 누락. `__init__.py`가 아니므로 패키지로 인식되지 않을 수 있다.
3. **의존성 명시 파일 없음** — `requirements.txt` / `pyproject.toml` 부재. 현재는 README의 수동 명령에 의존한다.
4. **빈 패키지** — `agora/app/__init__.py`, `agora/titanic/app/__init__.py` 등이 0바이트로 비어 있다 (정상). `caledon_validation.py`는 빈 클래스 (구현 예정).

---

## 라이선스

미정 (TBD).
