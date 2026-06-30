from pydantic import BaseModel, Field


class TelegramSendRequest(BaseModel):
    chat_id: str = Field(..., description="수신 채팅 ID 또는 @채널명")
    text: str = Field(..., description="전송할 메시지 내용")


class TelegramNotifyRequest(BaseModel):
    text: str = Field(..., description="전송할 메시지 내용")


class TelegramSendResponse(BaseModel):
    success: bool
    message: str


class TelegramMessengerSchema(BaseModel):
    id: int = Field(4, description="Telegram Service ID")
    name: str = Field("텔레그램 메신저 (Telegram Messenger)", description="서비스 이름")
