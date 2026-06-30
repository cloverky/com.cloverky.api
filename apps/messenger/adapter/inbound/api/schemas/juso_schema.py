from pydantic import BaseModel, ConfigDict, Field


class JusoSearchRequest(BaseModel):
    keyword: str = Field(..., description="검색할 주소 키워드")
    page: int = Field(1, ge=1, description="페이지 번호")
    count: int = Field(10, ge=1, le=100, description="페이지당 결과 수")


class JusoSearchResponse(BaseModel):
    total_count: int
    results: list[dict]


class JusoMessengerSchema(BaseModel):
    id: int = Field(2, description="Juso Service ID")
    name: str = Field("주소 검색기 (Juso Messenger)", description="서비스 이름")


class ContactRecordSchema(BaseModel):
    """Google Contacts CSV 한 행을 표현하는 스키마.

    헤더 순서:
    First Name, Middle Name, Last Name,
    Phonetic First Name, Phonetic Middle Name, Phonetic Last Name,
    Name Prefix, Name Suffix, Nickname, File As,
    Organization Name, Organization Title, Organization Department,
    Birthday, Notes, Photo, Labels,
    E-mail 1 - Label, E-mail 1 - Value,
    Phone 1 - Label, Phone 1 - Value
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    # 이름
    first_name: str = Field("", alias="First Name")
    middle_name: str = Field("", alias="Middle Name")
    last_name: str = Field("", alias="Last Name")
    phonetic_first_name: str = Field("", alias="Phonetic First Name")
    phonetic_middle_name: str = Field("", alias="Phonetic Middle Name")
    phonetic_last_name: str = Field("", alias="Phonetic Last Name")
    name_prefix: str = Field("", alias="Name Prefix")
    name_suffix: str = Field("", alias="Name Suffix")
    nickname: str = Field("", alias="Nickname")
    file_as: str = Field("", alias="File As")
    # 조직
    organization_name: str = Field("", alias="Organization Name")
    organization_title: str = Field("", alias="Organization Title")
    organization_department: str = Field("", alias="Organization Department")
    # 기타
    birthday: str = Field("", alias="Birthday")
    notes: str = Field("", alias="Notes")
    photo: str = Field("", alias="Photo")
    labels: str = Field("", alias="Labels")
    # 이메일
    email_label: str = Field("", alias="E-mail 1 - Label")
    email_value: str = Field("", alias="E-mail 1 - Value")
    # 전화
    phone_label: str = Field("", alias="Phone 1 - Label")
    phone_value: str = Field("", alias="Phone 1 - Value")

    @property
    def display_name(self) -> str:
        parts = [self.first_name, self.middle_name, self.last_name]
        full = " ".join(p for p in parts if p).strip()
        return full or self.nickname or self.file_as or self.organization_name
