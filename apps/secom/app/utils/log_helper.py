import logging
from typing import Any

from secom.app.schemas.user_schema import LoginSchema, UserSchema

logger = logging.getLogger("secom.save_user")


def mask_user_payload(user_schema: UserSchema) -> dict[str, Any]:
    """로그용 — 비밀번호는 마스킹."""
    data = user_schema.model_dump()
    pwd = data.get("password", "")
    data["password"] = f"*** (길이 {len(pwd)})" if pwd else "(비어 있음)"
    return data


def log_save_user_layer(layer: str, user_schema: UserSchema) -> None:
    payload = mask_user_payload(user_schema)
    logger.info(
        "[%s] save_user 레이어 통과 — username=%r name=%r email=%r role=%r password=%s",
        layer,
        user_schema.username,
        user_schema.name,
        user_schema.email,
        user_schema.role,
        payload["password"],
    )
    logger.debug("[%s] save_user 전체 payload=%s", layer, payload)


def mask_login_payload(login_schema: LoginSchema) -> dict[str, Any]:
    data = login_schema.model_dump()
    pwd = data.get("password", "")
    data["password"] = f"*** (길이 {len(pwd)})" if pwd else "(비어 있음)"
    return data


def log_login_layer(layer: str, login_schema: LoginSchema) -> None:
    payload = mask_login_payload(login_schema)
    logger.info(
        "[%s] login 레이어 통과 — email=%r password=%s",
        layer,
        login_schema.email,
        payload["password"],
    )
    logger.debug("[%s] login 전체 payload=%s", layer, payload)
