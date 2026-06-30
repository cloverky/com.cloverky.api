from dataclasses import dataclass
from enum import Enum


class EmailType(Enum):
    TEST = "test"
    NOTIFICATION = "notification"
    ALERT = "alert"
    REPORT = "report"


@dataclass(frozen=True)
class MailTemplate:
    instruction: str
    tone: str
    salutation: str  # 인사말 스타일
    intro: str       # 도입부 안내
    closing: str     # 맺음말 스타일


MAIL_TEMPLATES: dict[EmailType, MailTemplate] = {
    EmailType.TEST: MailTemplate(
        instruction="클로버키 서비스의 자동화 테스트 이메일",
        tone="친근하고 명확하게",
        salutation="안녕하세요.",
        intro="클로버키 자동화 시스템입니다.",
        closing="감사합니다.\n클로버키 드림",
    ),
    EmailType.NOTIFICATION: MailTemplate(
        instruction="클로버키 서비스 알림 이메일",
        tone="정중하고 간결하게",
        salutation="안녕하세요.",
        intro="클로버키 서비스 담당자입니다.",
        closing="감사합니다.\n클로버키 드림",
    ),
    EmailType.ALERT: MailTemplate(
        instruction="클로버키 서비스 긴급 알림 이메일",
        tone="명확하고 신속하게",
        salutation="안녕하세요.",
        intro="클로버키 운영팀입니다. 긴급 안내 사항을 전달드립니다.",
        closing="빠른 확인 부탁드립니다.\n클로버키 운영팀 드림",
    ),
    EmailType.REPORT: MailTemplate(
        instruction="클로버키 서비스 리포트 이메일",
        tone="전문적이고 객관적으로",
        salutation="안녕하세요.",
        intro="클로버키 서비스 리포트를 공유드립니다.",
        closing="검토 후 의견 주시면 감사하겠습니다.\n클로버키 드림",
    ),
}
