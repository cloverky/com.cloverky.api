from __future__ import annotations

import math
from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_rose_model_dto import (
    PassengerPredictionCommand,
    SurvivalPredictionResult,
)


class MLPredictionStrategy(ABC):
    @property
    @abstractmethod
    def algorithm_name(self) -> str: ...

    @abstractmethod
    def predict(
        self, command: PassengerPredictionCommand
    ) -> SurvivalPredictionResult: ...

    def _build_result(self, probability: float) -> SurvivalPredictionResult:
        p = max(0.0, min(1.0, probability))
        if p >= 0.7 or p <= 0.3:
            confidence = "high"
        elif p >= 0.6 or p <= 0.4:
            confidence = "medium"
        else:
            confidence = "low"
        return SurvivalPredictionResult(
            algorithm=self.algorithm_name,
            survived=p >= 0.5,
            probability=round(p, 4),
            confidence=confidence,
        )

    @staticmethod
    def _sigmoid(x: float) -> float:
        return 1.0 / (1.0 + math.exp(-x))

    @staticmethod
    def _family_size(command: PassengerPredictionCommand) -> int:
        return command.sibsp + command.parch + 1


# ──────────────────────────────────────────────
# 1. XGBoost — 그래디언트 부스팅 + 규제
# ──────────────────────────────────────────────
class XGBoostStrategy(MLPredictionStrategy):
    @property
    def algorithm_name(self) -> str:
        return "XGBoost"

    def predict(self, command: PassengerPredictionCommand) -> SurvivalPredictionResult:
        rounds = [self._round1(command), self._round2(command), self._round3(command)]
        return self._build_result(sum(rounds) / len(rounds))

    def _round1(self, c: PassengerPredictionCommand) -> float:
        score = 0.30
        score += 0.38 if c.sex == "female" else 0
        score += {1: 0.22, 2: 0.07, 3: -0.12}.get(c.pclass, 0)
        return max(0.0, min(1.0, score))

    def _round2(self, c: PassengerPredictionCommand) -> float:
        age = c.age if c.age > 0 else 28
        fs = self._family_size(c)
        score = 0.30
        score += 0.18 if age < 16 else (-0.05 if age > 60 else 0)
        score += 0.12 if 2 <= fs <= 4 else (-0.08 if fs >= 5 else 0)
        score += 0.10 if c.fare > 30 else (-0.05 if c.fare < 10 else 0)
        return max(0.0, min(1.0, score))

    def _round3(self, c: PassengerPredictionCommand) -> float:
        score = 0.30
        score += 0.30 if c.title in ("Miss", "Mrs", "Mme") else 0
        score += 0.12 if c.title == "Master" else 0
        score += 0.05 if c.embarked == "C" else 0
        return max(0.0, min(1.0, score))


# ──────────────────────────────────────────────
# 2. Random Forest — 다수 결정 트리 배깅
# ──────────────────────────────────────────────
class RandomForestStrategy(MLPredictionStrategy):
    @property
    def algorithm_name(self) -> str:
        return "RandomForest"

    def predict(self, command: PassengerPredictionCommand) -> SurvivalPredictionResult:
        trees = [
            self._tree_gender_class(command),
            self._tree_age_family(command),
            self._tree_fare_embark(command),
            self._tree_title(command),
            self._tree_combined(command),
        ]
        return self._build_result(sum(trees) / len(trees))

    def _tree_gender_class(self, c: PassengerPredictionCommand) -> float:
        if c.sex == "female":
            return 0.74 if c.pclass in (1, 2) else 0.50
        return 0.19 if c.pclass == 1 else 0.13

    def _tree_age_family(self, c: PassengerPredictionCommand) -> float:
        age = c.age if c.age > 0 else 28
        fs = self._family_size(c)
        if age < 10:
            return 0.60
        if fs >= 5:
            return 0.20
        return 0.45 if 2 <= fs <= 4 else 0.30

    def _tree_fare_embark(self, c: PassengerPredictionCommand) -> float:
        if c.fare > 50:
            return 0.65
        if c.fare > 15:
            return 0.45 if c.embarked in ("C", "Q") else 0.35
        return 0.20

    def _tree_title(self, c: PassengerPredictionCommand) -> float:
        return {
            "Miss": 0.72,
            "Mrs": 0.79,
            "Mme": 0.82,
            "Master": 0.58,
            "Mr": 0.16,
            "Dr": 0.42,
        }.get(c.title, 0.35)

    def _tree_combined(self, c: PassengerPredictionCommand) -> float:
        score = 0.35
        score += 0.30 if c.sex == "female" else 0
        score += {1: 0.18, 2: 0.05, 3: -0.10}.get(c.pclass, 0)
        return max(0.0, min(1.0, score))


# ──────────────────────────────────────────────
# 3. LightGBM — 리프 중심 트리 + 교호작용 항
# ──────────────────────────────────────────────
class LightGBMStrategy(MLPredictionStrategy):
    @property
    def algorithm_name(self) -> str:
        return "LightGBM"

    def predict(self, command: PassengerPredictionCommand) -> SurvivalPredictionResult:
        age = command.age if command.age > 0 else 28
        fs = self._family_size(command)
        is_female = command.sex == "female"

        score = 0.28
        score += 0.40 if is_female else 0
        score += {1: 0.22, 2: 0.08, 3: -0.12}.get(command.pclass, 0)
        # 교호작용: 성별 × 등급
        if is_female and command.pclass == 1:
            score += 0.10
        elif not is_female and command.pclass == 3:
            score -= 0.08
        score += 0.15 if age < 16 else 0
        score += 0.08 if 2 <= fs <= 4 else (-0.07 if fs >= 5 else 0)
        score += 0.06 if command.fare > 30 else 0
        return self._build_result(score)


# ──────────────────────────────────────────────
# 4. CatBoost — 범주형 피처 특화 부스팅
# ──────────────────────────────────────────────
class CatBoostStrategy(MLPredictionStrategy):
    @property
    def algorithm_name(self) -> str:
        return "CatBoost"

    def predict(self, command: PassengerPredictionCommand) -> SurvivalPredictionResult:
        sex_w = {"female": 0.70, "male": 0.17}.get(command.sex, 0.40)
        embark_w = {"C": 0.55, "Q": 0.40, "S": 0.33}.get(command.embarked, 0.38)
        title_w = {
            "Miss": 0.72,
            "Mrs": 0.78,
            "Mme": 0.82,
            "Master": 0.58,
            "Mr": 0.16,
            "Col": 0.48,
            "Major": 0.42,
            "Dr": 0.44,
        }.get(command.title, 0.35)
        class_w = {1: 0.63, 2: 0.47, 3: 0.24}.get(command.pclass, 0.38)

        prob = sex_w * 0.40 + class_w * 0.30 + title_w * 0.20 + embark_w * 0.10
        return self._build_result(prob)


# ──────────────────────────────────────────────
# 5. Logistic Regression — 선형 이진 분류
# ──────────────────────────────────────────────
class LogisticRegressionStrategy(MLPredictionStrategy):
    @property
    def algorithm_name(self) -> str:
        return "LogisticRegression"

    def predict(self, command: PassengerPredictionCommand) -> SurvivalPredictionResult:
        age = command.age if command.age > 0 else 28
        logit = (
            -1.20
            + (2.50 if command.sex == "female" else 0)
            + {1: 1.20, 2: 0.40, 3: 0.0}.get(command.pclass, 0)
            + (-0.02 * age)
            + (0.003 * command.fare)
            + (0.15 * (command.sibsp + command.parch))
            + (0.30 if command.embarked == "C" else 0)
        )
        return self._build_result(self._sigmoid(logit))


# ──────────────────────────────────────────────
# 6. Decision Tree — 명시적 규칙 기반 분류
# ──────────────────────────────────────────────
class DecisionTreeStrategy(MLPredictionStrategy):
    @property
    def algorithm_name(self) -> str:
        return "DecisionTree"

    def predict(self, command: PassengerPredictionCommand) -> SurvivalPredictionResult:
        return self._build_result(self._traverse(command))

    def _traverse(self, c: PassengerPredictionCommand) -> float:
        age = c.age if c.age > 0 else 28
        if c.sex == "female":
            if c.pclass in (1, 2):
                return 0.92 if age < 50 else 0.86
            return 0.72 if self._family_size(c) <= 3 else 0.46
        # male
        if age < 10:
            return 0.59 if c.pclass < 3 else 0.45
        if c.pclass == 1:
            return 0.40 if c.fare > 50 else 0.32
        return 0.18 if c.pclass == 2 else 0.12


# ──────────────────────────────────────────────
# 7. SVM — 최대 마진 초평면 (표준화 기준)
# ──────────────────────────────────────────────
class SVMStrategy(MLPredictionStrategy):
    @property
    def algorithm_name(self) -> str:
        return "SVM"

    def predict(self, command: PassengerPredictionCommand) -> SurvivalPredictionResult:
        age = command.age if command.age > 0 else 28
        age_z = (age - 29.7) / 14.5  # z-score (Titanic 통계 기반)
        fare_z = (command.fare - 32.2) / 49.7

        score = (
            -1.0 * age_z
            + 0.8 * fare_z
            + (1.8 if command.sex == "female" else -1.8)
            + {1: 1.0, 2: 0.2, 3: -1.2}.get(command.pclass, 0)
        )
        return self._build_result(self._sigmoid(score))


# ──────────────────────────────────────────────
# 8. KNN — K-최근접 이웃 (원형 승객 비교)
# ──────────────────────────────────────────────
class KNNStrategy(MLPredictionStrategy):
    @property
    def algorithm_name(self) -> str:
        return "KNN"

    _K = 5
    # (survived, pclass, sex, age, fare)
    _ARCHETYPES: list[tuple[bool, int, str, float, float]] = [
        (True, 1, "female", 35, 80),
        (True, 2, "female", 28, 23),
        (True, 1, "male", 40, 100),
        (True, 3, "female", 5, 10),
        (True, 1, "female", 50, 60),
        (False, 3, "male", 25, 8),
        (False, 2, "male", 30, 15),
        (False, 3, "female", 22, 7),
        (False, 3, "male", 40, 9),
        (False, 2, "male", 45, 14),
    ]

    def predict(self, command: PassengerPredictionCommand) -> SurvivalPredictionResult:
        age = command.age if command.age > 0 else 28
        distances: list[tuple[float, bool]] = []
        for survived, pclass, sex, arch_age, arch_fare in self._ARCHETYPES:
            d = (
                (0 if command.sex == sex else 2.0)
                + abs(command.pclass - pclass) * 1.5
                + abs(age - arch_age) / 10.0
                + abs(command.fare - arch_fare) / 30.0
            )
            distances.append((d, survived))

        nearest = sorted(distances, key=lambda x: x[0])[: self._K]
        prob = sum(1 for _, s in nearest if s) / self._K
        return self._build_result(prob)


# ──────────────────────────────────────────────
# 9. Naive Bayes — 독립 조건부 확률
# ──────────────────────────────────────────────
class NaiveBayesStrategy(MLPredictionStrategy):
    @property
    def algorithm_name(self) -> str:
        return "NaiveBayes"

    _PRIOR = 0.384  # Titanic 실제 생존율

    def predict(self, command: PassengerPredictionCommand) -> SurvivalPredictionResult:
        age = command.age if command.age > 0 else 28

        log_ratio = math.log(self._PRIOR / (1 - self._PRIOR))

        sex_p = 0.74 if command.sex == "female" else 0.19
        log_ratio += math.log(sex_p / (1 - sex_p))

        pclass_p = {1: 0.63, 2: 0.47, 3: 0.24}.get(command.pclass, 0.38)
        log_ratio += math.log(pclass_p / (1 - pclass_p))

        age_p = 0.55 if age < 16 else (0.42 if age < 40 else 0.35)
        log_ratio += math.log(age_p / (1 - age_p))

        emb_p = {"C": 0.55, "Q": 0.39, "S": 0.34}.get(command.embarked, 0.38)
        log_ratio += math.log(emb_p / (1 - emb_p))

        return self._build_result(self._sigmoid(log_ratio))


# ──────────────────────────────────────────────
# 10. K-Means + PCA — 군집화 보조 분류
# ──────────────────────────────────────────────
class KMeansPCAStrategy(MLPredictionStrategy):
    @property
    def algorithm_name(self) -> str:
        return "KMeans+PCA"

    # (pc1, pc2, survival_rate) — 2D PCA 공간 군집 중심
    _CLUSTERS: list[tuple[float, float, float]] = [
        (-2.1, 1.3, 0.78),  # 고생존: 1등급 여성
        (-0.8, 0.5, 0.62),  # 중생존: 2등급 여성
        (0.3, -0.4, 0.41),  # 혼합:   저가 요금 혼합
        (1.5, -1.2, 0.22),  # 저생존: 3등급 남성 성인
        (2.2, -2.0, 0.14),  # 최저:   고위험 그룹
    ]

    def predict(self, command: PassengerPredictionCommand) -> SurvivalPredictionResult:
        pc1, pc2 = self._project(command)
        best_survival = min(
            self._CLUSTERS,
            key=lambda c: math.sqrt((pc1 - c[0]) ** 2 + (pc2 - c[1]) ** 2),
        )[2]
        return self._build_result(best_survival)

    def _project(self, c: PassengerPredictionCommand) -> tuple[float, float]:
        age = c.age if c.age > 0 else 28
        gender = -1 if c.sex == "female" else 1
        fs = self._family_size(c)
        # PC1: 성별 + 등급 (주축)
        pc1 = 0.6 * gender + 0.5 * (c.pclass - 2) - 0.3 * (c.fare - 32) / 50
        # PC2: 나이 + 가족
        pc2 = 0.5 * (age - 30) / 15 - 0.4 * (fs - 2) / 3
        return pc1, pc2


# ──────────────────────────────────────────────
# 전략 레지스트리
# ──────────────────────────────────────────────
STRATEGY_REGISTRY: dict[str, MLPredictionStrategy] = {
    "xgboost": XGBoostStrategy(),
    "random_forest": RandomForestStrategy(),
    "lightgbm": LightGBMStrategy(),
    "catboost": CatBoostStrategy(),
    "logistic_regression": LogisticRegressionStrategy(),
    "decision_tree": DecisionTreeStrategy(),
    "svm": SVMStrategy(),
    "knn": KNNStrategy(),
    "naive_bayes": NaiveBayesStrategy(),
    "kmeans_pca": KMeansPCAStrategy(),
}
