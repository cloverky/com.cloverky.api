from datetime import datetime

from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    # 냉장고 식재료 관리 서비스의 사용자 스키마. default_storage로 기본 보관장소를 지정
    username: str = Field("", description="사용자명")
    name: str = Field("", description="이름")
    age: int = Field(0, description="나이")
    email: str = Field("", description="이메일")
    password_hash: str = Field("", description="비밀번호")
    role: str = Field("user", description="권한")
    fieldagree_terms: bool = Field(False, description="약관동의여부")
    default_storage: str = Field("냉장", description="기본 보관장소 (냉장·냉동·실온)")
    created_at: datetime | None = Field(None, description="생성일시")

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "cloverky",
                "name": "홍길동",
                "age": 28,
                "email": "user@example.com",
                "password_hash": "hashed_password",
                "role": "user",
                "fieldagree_terms": True,
                "default_storage": "냉장",
                "created_at": "2025-06-15T09:00:00Z",
            }
        }
    }
