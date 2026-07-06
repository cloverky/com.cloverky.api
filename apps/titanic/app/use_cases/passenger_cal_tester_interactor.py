from __future__ import annotations

import logging
from typing import Any

from titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import (
    CalTesterSchema,
)
from titanic.app.dtos.passenger_cal_tester_dto import CalTesterQuery, CalTesterResponse
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.app.ports.output.passenger_cal_tester_port import CalTesterPort
from titanic.app.use_cases._cal_testing import (
    evaluate_fitted_classifier,
    evaluate_fitted_kmeans_pca,
    rank_models,
)

logger = logging.getLogger(__name__)


class CalTesterInteractor(CalTesterUseCase):
    def __init__(self, repository: CalTesterPort):
        self.repository = repository

    async def test_model(self, test_set: dict[str, Any]) -> dict[str, Any]:
        """칼이 로즈가 제안한 10개 모델의 트레이닝 정도를 점수화해서 1등을 뽑는것.

        Args:
            test_set: Jack의 train_model 이 반환한 dict.
                      keys — X_test (ndarray), y_test (ndarray), trained_models (dict)
        """
        X_test = test_set["X_test"]
        y_test = test_set["y_test"]
        trained_models = test_set["trained_models"]

        test_results: dict[str, Any] = {}
        for name, fitted in trained_models.items():
            if name == "KMeans+PCA":
                test_results[name] = evaluate_fitted_kmeans_pca(fitted, X_test, y_test)
            else:
                test_results[name] = evaluate_fitted_classifier(fitted, X_test, y_test)
            logger.info(
                f"[CalTesterInteractor] {name} | "
                f"acc={test_results[name]['accuracy']} f1={test_results[name]['f1']}"
            )

        ranking = rank_models(test_results)
        best = ranking[0]["model"]

        return {
            "test_count": int(len(y_test)),
            "test_survived_rate": round(float(y_test.mean()), 4),
            "best_model": best,
            "ranking": ranking,
            "detail": test_results,
        }

    async def introduce_myself(self, schema: CalTesterSchema) -> CalTesterResponse:
        """칼 테스터의 자기소개 인터렉트"""
        return await self.repository.introduce_myself(
            CalTesterQuery(
                id=schema.id,
                name=schema.name,
            )
        )
