INTENT_MAP: dict[str, set[str]] = {
    "SURVIVAL_PREDICT": {
        # "생존" 제외 — 생존율(통계)과 겹침. 동사·확률 표현으로만 식별
        "예측", "살다", "죽다", "살아남다", "생존하다", "예측하다",
        "survive", "predict", "survived", "survival",
        "살았", "죽었", "가능성", "확률",
        "살", "죽", "살아", "살아남",
        "사",  # Kiwi: "살 수 있었을까" → 살다 stem "사"(VV) + ᆯ(ETM)
        "있을까", "살까", "됐을까", "됩니까", "될까",
    },
    "STATISTICS": {
        "통계", "비율", "얼마", "몇", "몇명", "명", "숫자",
        "stats", "statistics", "count", "rate", "percent",
        "전체", "합계", "평균", "총",
        "중요", "영향", "요인", "상관", "관계", "순위",
        "율",  # 생존율 → Kiwi: 생존(NNG) + 율(XSN)
    },
    "PASSENGER_SEARCH": {
        "찾다", "검색", "조회", "누구", "이름", "승객",
        "search", "find", "passenger", "who",
    },
    "MODEL_TRAIN": {
        "학습", "훈련", "모델", "알고리즘", "정확도", "성능",
        "train", "training", "model", "accuracy", "algorithm",
        "학습하다", "훈련하다", "결과",
    },
}
