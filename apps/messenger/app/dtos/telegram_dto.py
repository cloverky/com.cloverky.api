from dataclasses import dataclass


@dataclass
class TelegramSendCommand:
    chat_id: str
    text: str


@dataclass
class TelegramSendResult:
    success: bool
    message: str


@dataclass(frozen=True)
class TelegramMessengerQuery:
    id: int
    name: str


@dataclass(frozen=True)
class TelegramMessengerResponse:
    id: int
    name: str
    description: str
