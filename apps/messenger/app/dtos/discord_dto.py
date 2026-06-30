from dataclasses import dataclass


@dataclass
class DiscordSendCommand:
    content: str
    username: str = "FridgeAI"


@dataclass
class DiscordSendResult:
    success: bool
    message: str


@dataclass(frozen=True)
class DiscordMessengerQuery:
    id: int
    name: str


@dataclass(frozen=True)
class DiscordMessengerResponse:
    id: int
    name: str
    description: str
