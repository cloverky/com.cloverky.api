from dataclasses import dataclass, field


@dataclass
class JusoSearchCommand:
    keyword: str
    page: int = 1
    count: int = 10


@dataclass
class JusoResult:
    road_address: str
    jibun_address: str
    zip_code: str


@dataclass
class JusoSearchResult:
    total_count: int
    results: list[JusoResult] = field(default_factory=list)


@dataclass(frozen=True)
class JusoMessengerQuery:
    id: int
    name: str


@dataclass(frozen=True)
class JusoMessengerResponse:
    id: int
    name: str
    description: str


@dataclass
class ContactRecord:
    # 이름
    first_name: str
    middle_name: str
    last_name: str
    phonetic_first_name: str
    phonetic_middle_name: str
    phonetic_last_name: str
    name_prefix: str
    name_suffix: str
    nickname: str
    file_as: str
    # 조직
    organization_name: str
    organization_title: str
    organization_department: str
    # 기타
    birthday: str
    notes: str
    photo: str
    labels: str
    # 이메일
    email_1_label: str
    email_1_value: str
    # 전화
    phone_1_label: str
    phone_1_value: str


@dataclass
class ContactUploadCommand:
    records: list[ContactRecord]


@dataclass
class ContactUploadResult:
    saved: int
    skipped: int
