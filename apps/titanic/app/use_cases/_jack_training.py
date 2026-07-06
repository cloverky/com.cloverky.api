from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import (
    GradientBoostingClassifier,
    HistGradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

FEATURE_NAMES = [
    "pclass",
    "gender",
    "age",
    "sibsp",
    "parch",
    "fare",
    "family_size",
    "is_alone",
    "age_bin",
]


def clean_training_data(raw: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """결측·비정상 레코드 정리 및 타입 변환."""
    cleaned = []
    for row in raw:
        try:
            survived = _to_int(row.get("survived"))
            if survived not in (0, 1):
                continue
            cleaned.append(
                {
                    "pclass": _to_int(row.get("pclass")) or 3,
                    "gender": 1
                    if str(row.get("gender", "")).lower() in ("female", "f")
                    else 0,
                    "age": _to_float(row.get("age")),
                    "sibsp": _to_int(row.get("sibsp")) or 0,
                    "parch": _to_int(row.get("parch")) or 0,
                    "fare": _to_float(row.get("fare")),
                    "survived": survived,
                }
            )
        except Exception:
            continue

    # 결측 age / fare → 중앙값 대체
    ages = [r["age"] for r in cleaned if r["age"] is not None]
    fares = [r["fare"] for r in cleaned if r["fare"] is not None]
    age_med = float(np.median(ages)) if ages else 28.0
    fare_med = float(np.median(fares)) if fares else 14.5
    for r in cleaned:
        r["age"] = r["age"] if r["age"] is not None else age_med
        r["fare"] = r["fare"] if r["fare"] is not None else fare_med

    return cleaned


def build_feature_matrix(
    records: list[dict[str, Any]],
) -> tuple[np.ndarray, np.ndarray]:
    """피처 엔지니어링(titanic-algorithm.md) → 행렬 변환."""
    X_rows, y_rows = [], []
    for r in records:
        age = r["age"]
        family_size = r["sibsp"] + r["parch"] + 1
        age_bin = (
            0
            if age < 16
            else 1
            if age < 30
            else 2
            if age < 45
            else 3
            if age < 60
            else 4
        )
        X_rows.append(
            [
                r["pclass"],
                r["gender"],
                age,
                r["sibsp"],
                r["parch"],
                r["fare"],
                family_size,
                1 if family_size == 1 else 0,  # is_alone
                age_bin,
            ]
        )
        y_rows.append(r["survived"])
    return np.array(X_rows, dtype=float), np.array(y_rows, dtype=int)


def build_supervised_classifiers() -> dict[str, Any]:
    """로즈 제안 10대 알고리즘(titanic-algorithm.md) → sklearn 분류기.

    XGBoost/LightGBM/CatBoost는 요구 패키지가 없으므로
    sklearn 동치 모델로 대응한다.
    """
    return {
        # 1. XGBoost  → GradientBoostingClassifier (규제 포함 부스팅)
        "XGBoost": GradientBoostingClassifier(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=4,
            subsample=0.8,
            random_state=42,
        ),
        # 2. Random Forest
        "RandomForest": RandomForestClassifier(
            n_estimators=200,
            max_depth=6,
            random_state=42,
        ),
        # 3. LightGBM  → HistGradientBoostingClassifier (리프 중심 고속 부스팅)
        "LightGBM": HistGradientBoostingClassifier(
            max_iter=200,
            learning_rate=0.05,
            max_depth=4,
            random_state=42,
        ),
        # 4. CatBoost  → GradientBoostingClassifier (범주형 특화 파라미터)
        "CatBoost": GradientBoostingClassifier(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=5,
            min_samples_leaf=5,
            random_state=42,
        ),
        # 5. Logistic Regression (표준화 파이프라인)
        "LogisticRegression": Pipeline(
            [
                ("scaler", StandardScaler()),
                ("clf", LogisticRegression(max_iter=1000, random_state=42)),
            ]
        ),
        # 6. Decision Tree
        "DecisionTree": DecisionTreeClassifier(max_depth=5, random_state=42),
        # 7. SVM (표준화 필수)
        "SVM": Pipeline(
            [
                ("scaler", StandardScaler()),
                ("clf", SVC(kernel="rbf", C=1.0, random_state=42)),
            ]
        ),
        # 8. KNN (표준화 필수)
        "KNN": Pipeline(
            [
                ("scaler", StandardScaler()),
                ("clf", KNeighborsClassifier(n_neighbors=7)),
            ]
        ),
        # 9. Naive Bayes
        "NaiveBayes": GaussianNB(),
    }


def fit_supervised_classifiers(
    X_train: np.ndarray,
    y_train: np.ndarray,
    cv_folds: int = 5,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """각 분류기를 X_train으로 CV 평가 후 전체 학습 세트로 최종 피팅한다.

    Returns:
        fitted_models: 학습 완료된 분류기 dict (Cal에게 전달할 test_set에 포함)
        cv_results:    CV 정확도 요약 dict (Jack이 반환할 훈련 리포트)
    """
    fitted_models: dict[str, Any] = {}
    cv_results: dict[str, Any] = {}
    for name, clf in build_supervised_classifiers().items():
        scores = cross_val_score(clf, X_train, y_train, cv=cv_folds, scoring="accuracy")
        clf.fit(X_train, y_train)
        fitted_models[name] = clf
        cv_results[name] = {
            "cv_accuracy": round(float(scores.mean()), 4),
            "cv_std": round(float(scores.std()), 4),
        }
    return fitted_models, cv_results


def fit_kmeans_pca(X_train: np.ndarray, y_train: np.ndarray) -> dict[str, Any]:
    """KMeans+PCA를 학습 세트로 피팅하고 클러스터-생존 매핑까지 결정한다.

    Returns:
        scaler, pca, kmeans 객체와 survived_cluster 인덱스를 담은 dict.
        Cal이 transform → predict 시 재사용한다.
    """
    scaler = StandardScaler()
    X_s = scaler.fit_transform(X_train)
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_s)
    kmeans = KMeans(n_clusters=2, n_init=10, random_state=42)
    labels = kmeans.fit_predict(X_pca)
    rate_c0 = float(y_train[labels == 0].mean()) if (labels == 0).any() else 0.0
    rate_c1 = float(y_train[labels == 1].mean()) if (labels == 1).any() else 0.0
    return {
        "scaler": scaler,
        "pca": pca,
        "kmeans": kmeans,
        "survived_cluster": 0 if rate_c0 > rate_c1 else 1,
    }


def _to_int(val: Any) -> int | None:
    try:
        return int(float(str(val)))
    except (TypeError, ValueError):
        return None


def _to_float(val: Any) -> float | None:
    try:
        return float(str(val))
    except (TypeError, ValueError):
        return None
