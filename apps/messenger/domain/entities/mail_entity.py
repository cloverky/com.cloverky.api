from __future__ import annotations

from dataclasses import dataclass

from messenger.domain.value_objects.email_address_vo import EmailAddress
from messenger.domain.value_objects.mail_subject_vo import MailSubject


@dataclass
class Mail:
    recipient: EmailAddress
    subject: MailSubject
    body: str

    @classmethod
    def create(cls, to: str, subject: str, body: str) -> Mail:
        return cls(
            recipient=EmailAddress.from_raw(to),
            subject=MailSubject.from_raw(subject),
            body=body,
        )

    @property
    def to(self) -> str:
        return str(self.recipient)

    def is_valid(self) -> bool:
        return bool(self.body.strip())
