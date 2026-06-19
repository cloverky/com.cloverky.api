from __future__ import annotations

import logging
from typing import Any

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from titanic.adapter.outbound.orm.passenger_rose_model_strategies_orm import build_all_strategies
from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainerSchema
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from titanic.app.ports.output.passenger_jack_trainer_port import JackTrainerPort

logger = logging.getLogger(__name__)


class JackTrainerInteractor:

    def __init__(self, repository: JackTrainerPort):
        self.repository = repository
        self._trained_strategies: dict = {}

    async def train_model(self, train_set: pd.DataFrame) -> dict[str, Any]:
        '''로즈가 제안한 모델들을 훈련시키는 메소드'''
        logger.info("[JackTrainerInteractor] 학습 파이프라인 시작")

        

        X_train: list[list[float]] = train.value.tolist()

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # 8. 로즈의 10개 전략으로 학습
        self._trained_strategies = {}
        for key, StrategyClass in build_all_strategies().items():
            strategy = StrategyClass()
            try:
                strategy.fit(X_train.tolist(), y_train.tolist())
                self._trained_strategies[key] = strategy
                logger.info(f"[JackTrainerInteractor] {strategy.name} 학습 완료")
            except Exception as e:
                logger.warning(f"[JackTrainerInteractor] {key} 학습 실패 | error={e}")

        return {
            "train_samples": len(X_train),
            "trained_models": self._trained_strategies,
            "X_test": X_test,
            "y_test": y_test,
        }

    

    async def introduce_myself(self, schema: JackTrainerSchema) -> JackTrainerResponse:
        '''잭 트레이너의 자기소개 인터렉트'''
        return await self.repository.introduce_myself(JackTrainerQuery(
            id=schema.id,
            name=schema.name,
        ))