from __future__ import annotations

import asyncio
import logging

from messenger.app.dtos.watcher_dto import RoutingDecision, WatcherTriageCommand, WatcherTriageResult
from messenger.app.ports.input.receive_use_case import ReceiveUseCase
from messenger.app.ports.input.watcher_use_case import WatcherUseCase

logger = logging.getLogger(__name__)

_ESCALATION_KEYWORDS = {"보고서", "실적", "에스컬레이션", "report", "escalat"}

# KcELECTRA 파이프라인 — 최초 호출 시 1회 로드
_kcelectra_pipeline = None


def _get_filter_pipeline():
    global _kcelectra_pipeline
    if _kcelectra_pipeline is None:
        from transformers import pipeline as hf_pipeline
        _kcelectra_pipeline = hf_pipeline(
            "text-classification",
            model="smilegate-ai/kor_unsmile",
            tokenizer="smilegate-ai/kor_unsmile",
            top_k=None,
        )
    return _kcelectra_pipeline


class WatcherInteractor(WatcherUseCase):
    def __init__(self, receive: ReceiveUseCase) -> None:
        self._receive = receive

    async def triage(self, command: WatcherTriageCommand) -> WatcherTriageResult:
        text = " ".join(filter(None, [command.subject, command.body]))

        # Step 1 — KcELECTRA 정책 필터링
        is_blocked = await asyncio.to_thread(self._is_offensive, text)
        if is_blocked:
            logger.warning("[Watson] 정책 위반 감지 — from=%r, 이벤트 폐기", command.from_email)
            return WatcherTriageResult(routing=RoutingDecision.BLOCKED, reason="정책 위반 — 비속어/욕설 감지")

        # Step 2 — 라우팅 분류
        routing, reason = self._classify(command)
        logger.info("[Watson] triage — from=%r routing=%s reason=%s", command.from_email, routing.value, reason)

        # Step 3 — Holmes 경로: pgvector 임베딩 파이프라인으로 전달
        if routing == RoutingDecision.HOLMES and text and command.mail_id is not None:
            asyncio.create_task(self._receive.embed_and_store(command.mail_id, text))

        return WatcherTriageResult(routing=routing, reason=reason)

    async def filter_stop_word(self, text: str) -> bool:
        """비속어 필터링 하는 모델"""
        return await asyncio.to_thread(self._is_offensive, text)

    @staticmethod
    def _is_offensive(text: str) -> bool:
        if not text.strip():
            return False
        results = _get_filter_pipeline()(text, truncation=True, max_length=512)[0]
        # clean 레이블 점수가 0.8 미만이면 혐오/비속어로 판단
        clean_score = next((r["score"] for r in results if r["label"] == "clean"), 0.0)
        return clean_score < 0.8

    @staticmethod
    def _classify(command: WatcherTriageCommand) -> tuple[RoutingDecision, str]:
        if command.important_client:
            return RoutingDecision.FAKER, "중요 거래처 — Faker 에스컬레이션"

        text = " ".join(filter(None, [command.subject, command.body])).lower()
        if any(kw in text for kw in _ESCALATION_KEYWORDS):
            return RoutingDecision.FAKER, "에스컬레이션 키워드 감지 — Faker 에스컬레이션"

        return RoutingDecision.HOLMES, "일반 메일 — Holmes 자체 처리"
