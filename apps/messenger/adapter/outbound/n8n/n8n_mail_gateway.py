from __future__ import annotations

import os

import httpx
from messenger.app.ports.output.mail_gateway import MailGateway


class N8nMailGateway(MailGateway):
    def __init__(self) -> None:
        self._webhook_url = os.getenv("N8N_MAIL_WEBHOOK_URL", "")

    async def send(self, to: str, subject: str, body: str) -> None:
        html_body = body.replace("\n", "<br>")
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self._webhook_url,
                json={"to": to, "subject": subject, "body": html_body},
            )
            response.raise_for_status()
