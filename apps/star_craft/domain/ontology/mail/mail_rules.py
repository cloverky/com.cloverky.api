from star_craft.domain.ontology.mail.mail_taxonomy import MAIL_TEMPLATES, EmailType

_STRUCTURE = """
비즈니스 이메일 작성 규칙:
각 단락 사이에 반드시 빈 줄을 넣는다.

구조:
인사말 → 빈 줄 → 도입부(발신자 소개 + 목적) → 빈 줄 → 본론 → 빈 줄 → 맺음말(감사 + 서명)

절대 금지:
- **, *, #, --- 등 마크다운 기호
- [※...], [이하...], [서명], [작업...] 등 대괄호 태그
- 번호 목록(1. 2. 3.)
- 분석·설명·주석 텍스트
- "도입부:", "본론:", "맺음말:", "인사말:", "서론:", "결론:" 등 구조 레이블 (절대 사용 금지)
- 이메일 본문 외 다른 모든 텍스트

출력: 이메일 본문 텍스트만. 다른 것은 아무것도 출력하지 않는다.
"""


def build_prompt(email_type: EmailType, context: str) -> str:
    t = MAIL_TEMPLATES[email_type]
    return (
        f"역할: {t.instruction}을 작성한다.\n"
        f"어조: {t.tone}\n"
        f"인사말 예시: {t.salutation}\n"
        f"도입부 예시: {t.intro}\n"
        f"맺음말 예시: {t.closing}\n"
        f"전달할 내용: {context}\n"
        f"{_STRUCTURE}"
    )
