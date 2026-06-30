from pydantic import BaseModel, Field

from star_craft.domain.ontology.mail.mail_taxonomy import EmailType


class MailRequest(BaseModel):
    to: str
    subject: str
    context: str
    email_type: EmailType = EmailType.NOTIFICATION


class MailResponse(BaseModel):
    success: bool
    message: str


class MailMessengerSchema(BaseModel):
    id: int = Field(1, description="Messenger ID")
    name: str = Field("메신저 (Mail Messenger)", description="서비스 이름")
