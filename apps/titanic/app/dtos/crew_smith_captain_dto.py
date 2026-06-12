from dataclasses import dataclass


@dataclass(frozen=True)
class SmithCaptainQuery:
    id: int
    name: str

@dataclass(frozen=True)
class SmithCaptainResponse:
    id: int
    name: str

@dataclass(frozen=True)
class SmithChatResponse:
    reply: str
