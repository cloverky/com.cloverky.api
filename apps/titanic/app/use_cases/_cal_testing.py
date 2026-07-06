from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.preprocessing import StandardScaler


def evaluate_classifier(
    clf,
    X_train: np.ndarray,
    X_test: np.ndarray,
    y_train: np.ndarray,
    y_test: np.ndarray,
) -> dict[str, Any]:
    """분류기를 학습 세트로 훈련 후 테스트 세트 평가 리포트 생성."""
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    try:
        y_proba = clf.predict_proba(X_test)[:, 1]
        auc: float | None = round(float(roc_auc_score(y_test, y_proba)), 4)
    except AttributeError:
        auc = None

    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    return {
        "accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
        "precision": round(float(precision_score(y_test, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, y_pred, zero_division=0)), 4),
        "f1": round(float(f1_score(y_test, y_pred, zero_division=0)), 4),
        "roc_auc": auc,
        "confusion_matrix": {
            "tn": int(tn),
            "fp": int(fp),
            "fn": int(fn),
            "tp": int(tp),
        },
    }


def evaluate_kmeans_pca(
    X_train: np.ndarray,
    X_test: np.ndarray,
    y_train: np.ndarray,
    y_test: np.ndarray,
) -> dict[str, Any]:
    """KMeans+PCA 비지도 모델을 학습 세트로 피팅 후 테스트 세트 평가."""
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    pca = PCA(n_components=2)
    X_train_pca = pca.fit_transform(X_train_s)
    X_test_pca = pca.transform(X_test_s)

    kmeans = KMeans(n_clusters=2, n_init=10, random_state=42)
    train_labels = kmeans.fit_predict(X_train_pca)

    # 학습 세트 기준 클러스터 → 생존 레이블 매핑
    rate_c0 = (
        float(y_train[train_labels == 0].mean()) if (train_labels == 0).any() else 0.0
    )
    rate_c1 = (
        float(y_train[train_labels == 1].mean()) if (train_labels == 1).any() else 0.0
    )
    survived_cluster = 0 if rate_c0 > rate_c1 else 1

    test_labels = kmeans.predict(X_test_pca)
    y_pred = (test_labels == survived_cluster).astype(int)

    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    return {
        "accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
        "precision": round(float(precision_score(y_test, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, y_pred, zero_division=0)), 4),
        "f1": round(float(f1_score(y_test, y_pred, zero_division=0)), 4),
        "roc_auc": None,
        "confusion_matrix": {
            "tn": int(tn),
            "fp": int(fp),
            "fn": int(fn),
            "tp": int(tp),
        },
        "pca_explained_variance": [
            round(float(v), 4) for v in pca.explained_variance_ratio_
        ],
    }


def evaluate_fitted_classifier(
    fitted_clf,
    X_test: np.ndarray,
    y_test: np.ndarray,
) -> dict[str, Any]:
    """Jack이 이미 학습시킨 분류기를 테스트 세트에서만 평가한다 (재학습 없음)."""
    y_pred = fitted_clf.predict(X_test)
    try:
        y_proba = np.array(fitted_clf.predict_proba(X_test))
        auc: float | None = round(float(roc_auc_score(y_test, y_proba)), 4)
    except (AttributeError, ValueError):
        auc = None
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    return {
        "accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
        "precision": round(float(precision_score(y_test, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, y_pred, zero_division=0)), 4),
        "f1": round(float(f1_score(y_test, y_pred, zero_division=0)), 4),
        "roc_auc": auc,
        "confusion_matrix": {
            "tn": int(tn),
            "fp": int(fp),
            "fn": int(fn),
            "tp": int(tp),
        },
    }


def evaluate_fitted_kmeans_pca(
    fitted: dict[str, Any],
    X_test: np.ndarray,
    y_test: np.ndarray,
) -> dict[str, Any]:
    """Jack이 피팅한 scaler/PCA/KMeans를 그대로 사용해 테스트 세트를 평가한다."""
    X_s = fitted["scaler"].transform(X_test)
    X_pca = fitted["pca"].transform(X_s)
    labels = fitted["kmeans"].predict(X_pca)
    y_pred = (labels == fitted["survived_cluster"]).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    return {
        "accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
        "precision": round(float(precision_score(y_test, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, y_pred, zero_division=0)), 4),
        "f1": round(float(f1_score(y_test, y_pred, zero_division=0)), 4),
        "roc_auc": None,
        "confusion_matrix": {
            "tn": int(tn),
            "fp": int(fp),
            "fn": int(fn),
            "tp": int(tp),
        },
    }


def rank_models(results: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """F1 점수 기준 내림차순 모델 순위 반환."""
    ranked = sorted(
        [{"rank": 0, "model": name, **metrics} for name, metrics in results.items()],
        key=lambda x: x["f1"],
        reverse=True,
    )
    for i, row in enumerate(ranked, 1):
        row["rank"] = i
    return ranked
