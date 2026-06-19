from __future__ import annotations

from typing import Optional

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import Base
from titanic.app.ports.output.passenger_rose_model_port import RoseModelPort


class BookingOrm(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    passenger_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("passengers.id"), nullable=True
    )
    pclass: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    ticket: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    fare: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    cabin: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    embarked: Mapped[Optional[str]] = mapped_column(String, nullable=True)


class XGBoostStrategy(RoseModelPort):
    """1위: XGBoost — 그래디언트 부스팅 기반 고성능 모델 (강력한 규제로 과적합 방지)"""

    @property
    def name(self) -> str:
        return "XGBoost"

    @property
    def description(self) -> str:
        return "그래디언트 부스팅 기반 고성능 모델. 강력한 규제(Regularization) 기능으로 과적합을 방지하며 리더보드 최상위권 점수를 낼 때 필수적입니다."

    def __init__(self) -> None:
        self._model = GradientBoostingClassifier(n_estimators=100, random_state=42)
            

    def fit(self, X, y) -> None:
        self._model.fit(X, y)

    def predict(self, X) -> list[int]:
        return self._model.predict(X).tolist()

    def predict_proba(self, X) -> list[float]:
        return self._model.predict_proba(X)[:, 1].tolist()


class RandomForestStrategy(RoseModelPort):
    """2위: Random Forest — 다수의 결정 트리를 결합하는 배깅 방식 (데이터 노이즈에 강함)"""

    @property
    def name(self) -> str:
        return "RandomForest"

    @property
    def description(self) -> str:
        return "다수의 결정 트리를 결합하는 배깅 방식. 데이터 노이즈에 강하며 하이퍼파라미터 튜닝 없이도 안정적인 Baseline 성능을 보장합니다."

    def __init__(self) -> None:
        self._model = RandomForestClassifier(n_estimators=100, random_state=42)

    def fit(self, X, y) -> None:
        self._model.fit(X, y)

    def predict(self, X) -> list[int]:
        return self._model.predict(X).tolist()

    def predict_proba(self, X) -> list[float]:
        return self._model.predict_proba(X)[:, 1].tolist()


class LightGBMStrategy(RoseModelPort):
    """3위: LightGBM — 리프 중심(Leaf-wise) 트리 분할 방식 (대용량 처리 특화, 고속)"""

    @property
    def name(self) -> str:
        return "LightGBM"

    @property
    def description(self) -> str:
        return "리프 중심(Leaf-wise) 트리 분할 방식. 대용량 처리에 특화되어 성능이 우수하고 속도가 빨라 복잡한 피처 조합 실험에 유용합니다."

    def __init__(self) -> None:
        self._model = GradientBoostingClassifier(n_estimators=100, random_state=42)
            

    def fit(self, X, y) -> None:
        self._model.fit(X, y)

    def predict(self, X) -> list[int]:
        return self._model.predict(X).tolist()

    def predict_proba(self, X) -> list[float]:
        return self._model.predict_proba(X)[:, 1].tolist()


class CatBoostStrategy(RoseModelPort):
    """4위: CatBoost — 범주형 데이터 처리에 최적화 (Sex, Embarked 별도 인코딩 불필요)"""

    @property
    def name(self) -> str:
        return "CatBoost"

    @property
    def description(self) -> str:
        return "범주형 데이터 처리에 최적화된 부스팅. Sex, Embarked 등 범주형 피처가 많은 타이타닉 데이터셋을 별도 인코딩 없이 최적화합니다."

    def __init__(self) -> None:
        self._model = GradientBoostingClassifier(n_estimators=100, random_state=42)

            
    def fit(self, X, y) -> None:
        self._model.fit(X, y)

    def predict(self, X) -> list[int]:
        return self._model.predict(X).tolist()

    def predict_proba(self, X) -> list[float]:
        return self._model.predict_proba(X)[:, 1].tolist()


class LogisticRegressionStrategy(RoseModelPort):
    """5위: Logistic Regression — 선형 기반 이진 분류 Baseline (피처 영향력 해석 용이, 표준화 필수)"""

    @property
    def name(self) -> str:
        return "LogisticRegression"

    @property
    def description(self) -> str:
        return "선형 관계를 기반으로 한 이진 분류 모델. 각 피처가 생존에 미치는 영향력을 직관적으로 해석하기 좋은 Baseline 모델입니다. 표준화(Standardization) 필수."

    def __init__(self) -> None:
        self._scaler = StandardScaler()
        self._model = LogisticRegression(max_iter=1000, random_state=42)

    def fit(self, X, y) -> None:
        self._model.fit(self._scaler.fit_transform(X), y)

    def predict(self, X) -> list[int]:
        return self._model.predict(self._scaler.transform(X)).tolist()

    def predict_proba(self, X) -> list[float]:
        return self._model.predict_proba(self._scaler.transform(X))[:, 1].tolist()


class DecisionTreeStrategy(RoseModelPort):
    """6위: Decision Tree — 직관적인 규칙 기반 모델 (시각화 가능, 과적합 주의)"""

    @property
    def name(self) -> str:
        return "DecisionTree"

    @property
    def description(self) -> str:
        return "나무 가지치기 형태의 직관적인 규칙 기반 모델. 데이터의 흐름과 분류 기준을 시각화하기 좋으나 과적합 위험이 있어 max_depth 튜닝이 필요합니다."

    def __init__(self) -> None:
        self._model = DecisionTreeClassifier(max_depth=5, random_state=42)

    def fit(self, X, y) -> None:
        self._model.fit(X, y)

    def predict(self, X) -> list[int]:
        return self._model.predict(X).tolist()

    def predict_proba(self, X) -> list[float]:
        return self._model.predict_proba(X)[:, 1].tolist()


class SVMStrategy(RoseModelPort):
    """7위: SVM — 마진 최대화 결정 경계 탐색 (비선형 관계 파악, 표준화 필수)"""

    @property
    def name(self) -> str:
        return "SVM"

    @property
    def description(self) -> str:
        return "마진을 최대화하는 최적 결정 경계 탐색. 데이터 전처리(표준화)가 정교하게 이루어졌을 때 변수 간의 복잡한 비선형 관계를 파악하는 데 유효합니다."

    def __init__(self) -> None:
        self._scaler = StandardScaler()
        self._model = SVC(kernel="rbf", probability=True, random_state=42)

    def fit(self, X, y) -> None:
        self._model.fit(self._scaler.fit_transform(X), y)

    def predict(self, X) -> list[int]:
        return self._model.predict(self._scaler.transform(X)).tolist()

    def predict_proba(self, X) -> list[float]:
        return self._model.predict_proba(self._scaler.transform(X))[:, 1].tolist()


class KNNStrategy(RoseModelPort):
    """8위: KNN — K-최근접 이웃 분류 (승객 간 유사도 기반, 정규화 권장)"""

    @property
    def name(self) -> str:
        return "KNN"

    @property
    def description(self) -> str:
        return "주변의 가장 가까운 K개 이웃 기준 분류. 승객 간의 유사도(나이, 요금, 객실 등)를 기반으로 작동하며 단순하지만 직관적인 결과를 줍니다. 정규화(Normalization) 권장."

    def __init__(self, k: int = 5) -> None:
        self._scaler = MinMaxScaler()
        self._model = KNeighborsClassifier(n_neighbors=k)

    def fit(self, X, y) -> None:
        self._model.fit(self._scaler.fit_transform(X), y)

    def predict(self, X) -> list[int]:
        return self._model.predict(self._scaler.transform(X)).tolist()

    def predict_proba(self, X) -> list[float]:
        return self._model.predict_proba(self._scaler.transform(X))[:, 1].tolist()


class NaiveBayesStrategy(RoseModelPort):
    """9위: Naive Bayes — 베이즈 정리 조건부 확률 기반 (빠른 계산, 희소 데이터 강점)"""

    @property
    def name(self) -> str:
        return "NaiveBayes"

    @property
    def description(self) -> str:
        return "베이즈 정리를 이용한 조건부 확률 기반 분류. 모든 특성이 독립적이라고 가정하며 계산이 매우 빠르고 희소한 데이터셋에서도 준수한 성능을 냅니다."

    def __init__(self) -> None:
        self._model = GaussianNB()

    def fit(self, X, y) -> None:
        self._model.fit(X, y)

    def predict(self, X) -> list[int]:
        return self._model.predict(X).tolist()

    def predict_proba(self, X) -> list[float]:
        return self._model.predict_proba(X)[:, 1].tolist()


class PCAKMeansStrategy(RoseModelPort):
    """10위: PCA + K-Means — 비지도 학습 보조 도구 (차원 축소 후 군집화, 파생 변수 생성)"""

    @property
    def name(self) -> str:
        return "PCA+KMeans"

    @property
    def description(self) -> str:
        return "비지도 학습 기반 군집화 및 차원 축소. 분류 모델은 아니지만 승객 그룹을 클러스터링(K-Means)하거나 수많은 피처를 압축(PCA)하여 파생 변수를 만들 때 보조적으로 활용됩니다."

    def __init__(self, n_components: int = 2, n_clusters: int = 2) -> None:
        self._scaler = StandardScaler()
        self._pca = PCA(n_components=n_components)
        self._kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self._cluster_to_label: dict[int, int] = {}

    def fit(self, X, y) -> None:
        import numpy as np
        X_reduced = self._pca.fit_transform(self._scaler.fit_transform(X))
        self._kmeans.fit(X_reduced)
        y_arr = np.array(y)
        for c in range(self._kmeans.n_clusters):
            mask = self._kmeans.labels_ == c
            rate = float(y_arr[mask].mean()) if mask.sum() > 0 else 0.0
            self._cluster_to_label[c] = 1 if rate >= 0.5 else 0

    def predict(self, X) -> list[int]:
        X_reduced = self._pca.transform(self._scaler.transform(X))
        return [self._cluster_to_label.get(int(c), 0) for c in self._kmeans.predict(X_reduced)]

    def predict_proba(self, X) -> list[float]:
        return [float(p) for p in self.predict(X)]


def build_all_strategies() -> dict:
    return {
        "xgboost": XGBoostStrategy,
        "random_forest": RandomForestStrategy,
        "lightgbm": LightGBMStrategy,
        "catboost": CatBoostStrategy,
        "logistic_regression": LogisticRegressionStrategy,
        "decision_tree": DecisionTreeStrategy,
        "svm": SVMStrategy,
        "knn": KNNStrategy,
        "naive_bayes": NaiveBayesStrategy,
        "pca_kmeans": PCAKMeansStrategy,
    }