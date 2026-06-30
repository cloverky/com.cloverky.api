from __future__ import annotations

import logging
import re

from messenger.app.ports.output.mail_gateway import MailGateway

from core.lol.t1_mid_faker_orchestrator import FakerOrchestrator
from star_craft.domain.ontology.mail.mail_rules import build_prompt
from star_craft.domain.ontology.mail.mail_taxonomy import EmailType

logger = logging.getLogger(__name__)

_TAG_PATTERN = re.compile(r"\[.*?\]")
_MARKDOWN_PATTERN = re.compile(r"(\*\*|__|##|---)")
_LABEL_PATTERN = re.compile(
    r"^(도입부|본론|맺음말|인사말|서론|결론|내용|요약)\s*:\s*", re.MULTILINE
)


def _clean(text: str) -> str:
    lines = []
    for line in text.splitlines():
        line = _TAG_PATTERN.sub("", line)
        line = _MARKDOWN_PATTERN.sub("", line)
        line = _LABEL_PATTERN.sub("", line)
        lines.append(line.rstrip())
    return "\n".join(lines).strip()


class MailOrchestrator:
    def __init__(self, gateway: MailGateway, llm: FakerOrchestrator) -> None:
        self._gateway = gateway
        self._llm = llm

    async def compose_and_send(
        self, to: str, subject: str, context: str, email_type: EmailType
    ) -> str:
        prompt = build_prompt(email_type=email_type, context=context)
        raw = await self._llm.achat([{"role": "user", "content": prompt}])
        body = _clean(raw)
        await self._gateway.send(to=to, subject=subject, body=body)
        logger.info(
            "[star_craft] 메일 발송 완료 | type=%s | to=%s | subject=%s",
            email_type.value,
            to,
            subject,
        )
        return body
