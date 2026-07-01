from __future__ import annotations

import json
import logging
import os

from pywebpush import WebPushException, webpush

logger = logging.getLogger(__name__)

_PRIVATE_KEY = os.getenv("VAPID_PRIVATE_KEY", "")
_CLAIMS_EMAIL = os.getenv("VAPID_CLAIMS_EMAIL", "mailto:admin@example.com")


def send_push(endpoint: str, p256dh: str, auth: str, title: str, body: str) -> bool:
    try:
        webpush(
            subscription_info={"endpoint": endpoint, "keys": {"p256dh": p256dh, "auth": auth}},
            data=json.dumps({"title": title, "body": body}),
            vapid_private_key=_PRIVATE_KEY,
            vapid_claims={"sub": _CLAIMS_EMAIL},
        )
        return True
    except WebPushException as e:
        logger.warning("Push 전송 실패 — endpoint: %r, error: %s", endpoint[:40], e)
        return False
