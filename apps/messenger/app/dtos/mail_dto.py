from dataclasses import dataclass

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
