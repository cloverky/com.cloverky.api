from pydantic import BaseModel, Field


class DiscordSendRequest(BaseModel):
    content: str = Field(..., description="전송할 메시지 내용")
    username: str = Field("FridgeAI", description="웹훅 표시 이름")


class DiscordSendResponse(BaseModel):
    success: bool
    message: str


class DiscordMessengerSchema(BaseModel):
    id: int = Field(3, description="Discord Service ID")
    name: str = Field("디스코드 메신저 (Discord Messenger)", description="서비스 이름")
