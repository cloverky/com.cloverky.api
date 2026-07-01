from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from star_craft.domain.ontology.mail.mail_taxonomy import EmailType


@dataclass
class MailCommand:
    to: str
    subject: str
    context: str
    email_type: EmailType = EmailType.NOTIFICATION


@dataclass
class MailResult:
    success: bool
    message: str


@dataclass(frozen=True)
class MailMessengerQuery:
    id: int
    name: str


@dataclass(frozen=True)
class MailMessengerResponse:
    id: int
    name: str
    description: str


@dataclass
class MailInboxReceiveCommand:
    from_email: str
    subject: str | None
    body: str | None


@dataclass(frozen=True)
class MailInboxItem:
    id: int
    from_email: str
    subject: str | None
    body: str | None
    received_at: datetime


@dataclass
class MailInboxListResult:
    items: list[MailInboxItem] = field(default_factory=list)
