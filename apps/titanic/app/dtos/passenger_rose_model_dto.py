from dataclasses import dataclass, field

@dataclass(frozen=True) # 생성 후 수정 불가하도록 설정
class RoseModelQuery:

    id: int   # 직관적인 타입 변경
    name: str


@dataclass(frozen=True) # 생성 후 수정 불가하도록 설정
class RoseModelResponse:

    id: int   # 직관적인 타입 변경
    name: str


@dataclass
class BookingCommand:

    pclass: str
    ticket: str
    fare: str
    cabin: str
    embarked: str


@dataclass(frozen=True)
class PassengerPredictionCommand:
    pclass: int       # 객실 등급 (1·2·3)
    sex: str          # "male" | "female"
    age: float        # 나이 (0 이하면 미입력)
    fare: float       # 운임
    sibsp: int        # 형제자매·배우자 수
    parch: int        # 부모·자녀 수
    embarked: str     # 승선지 "S" | "C" | "Q"
    title: str = field(default="")  # 이름에서 추출한 호칭


@dataclass(frozen=True)
class SurvivalPredictionResult:
    algorithm: str    # 사용된 알고리즘 이름
    survived: bool    # 생존 예측
    probability: float  # 생존 확률 (0.0 ~ 1.0)
    confidence: str   # "high" | "medium" | "low"
    