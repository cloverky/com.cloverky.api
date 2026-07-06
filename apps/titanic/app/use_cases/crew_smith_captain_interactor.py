from __future__ import annotations

import logging
import re
from typing import Any

import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import (
    ChatSchema,
    SmithCaptainSchema,
)
from titanic.app.dtos.crew_smith_captain_dto import (
    SmithCaptainQuery,
    SmithCaptainResponse,
    SmithChatResponse,
)
from titanic.app.ports.input.crew_andrews_architect_use_case import (
    AndrewsArchitectUseCase,
)
from titanic.app.ports.input.crew_hartley_violin_use_case import HartleyViolinUseCase
from titanic.app.ports.input.crew_lowe_boat_use_case import LoweBoatUseCase
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.output.crew_smith_captain_port import SmithCaptainPort

logger = logging.getLogger(__name__)

_FEATURE_COLS = [
    "Pclass",
    "gender",
    "SibSp",
    "Parch",
    "Embarked",
    "Title",
    "AgeGroup",
    "FareBand",
    "Deck",
]

_AGE_LABELS = {
    0: "Unknown",
    1: "Baby (0~5세)",
    2: "Child (6~12세)",
    3: "Teen (13~18세)",
    4: "Student (19~24세)",
    5: "Young Adult (25~35세)",
    6: "Adult (36~60세)",
    7: "Senior (61세+)",
}

_FEAT_LABELS = {
    "Pclass": "PClass(티켓 등급)",
    "gender": "Gender(성별)",
    "SibSp": "SibSp(형제·배우자 수)",
    "Parch": "Parch(부모·자녀 수)",
    "Embarked": "Embarkation(탑승항)",
    "Title": "Title(호칭)",
    "AgeGroup": "Age(나이)",
    "FareBand": "Fare(운임)",
    "Deck": "Cabin(객실 구역)",
}


class SmithCaptainInteractor(SmithCaptainUseCase):
    def __init__(
        self,
        repository: SmithCaptainPort,
        andrews: AndrewsArchitectUseCase,
        jack: JackTrainerUseCase,
        rose: RoseModelUseCase,
        cal: CalTesterUseCase,
        walter: WalterRoasterUseCase,
        lowe: LoweBoatUseCase,
        hartley: HartleyViolinUseCase,
    ):
        self.repository = repository
        self.andrews = andrews
        self.jack = jack
        self.rose = rose
        self.cal = cal
        self.walter = walter
        self.lowe = lowe
        self.hartley = hartley

    # ─── 메인 진입점 ──────────────────────────────────────────────────

    async def chat(self, schema: ChatSchema) -> SmithChatResponse:
        question = schema.message
        intent_result = self.andrews.analyze_intent(question)
        intent = intent_result["intent"]
        logger.info(f"[Smith] intent={intent} question={question!r}")

        train_set: DataFrame = await self.walter.get_train_set()

        # "X별" 패턴(나이별, 성별, 등급별) → 그룹별 통계
        if "별" in question:
            return SmithChatResponse(reply=self._answer_breakdown(train_set, question))

        # 나이+성별이 모두 추출되면 예측 우선 (intent 오분류 보완)
        attrs = self._extract_attrs(question)
        if attrs.get("age") and attrs.get("gender"):
            return SmithChatResponse(reply=self._answer_prediction(train_set, question))

        if intent == "STATISTICS":
            if any(
                w in question
                for w in [
                    "몇명",
                    "몇 명",
                    "몇명이나",
                    "몇명이",
                    "몇 명이",
                    "명이나",
                    "인원",
                    "탑승객 수",
                ]
            ):
                return SmithChatResponse(reply=await self._answer_count(train_set))
            return SmithChatResponse(reply=self._answer_statistics(train_set))
        if intent == "SURVIVAL_PREDICT":
            return SmithChatResponse(reply=self._answer_prediction(train_set, question))
        if intent == "MODEL_TRAIN":
            return SmithChatResponse(reply=self._answer_model(train_set))
        if intent == "PASSENGER_SEARCH":
            return SmithChatResponse(reply="승객 검색 기능은 준비 중입니다.")

        total = await self.walter.get_total_count()
        return SmithChatResponse(
            reply=(
                f"총 {total:,}명의 탑승객 데이터가 있습니다.\n"
                "예: '생존율에 가장 영향을 미친 요소가 뭐야?'  또는  '33세 남자라면 살 수 있었을까?'"
            )
        )

    # ─── 피처 엔지니어링 ───────────────────────────────────────────────

    def _engineer(self, raw: DataFrame) -> DataFrame:
        d = raw.copy().replace("", pd.NA).dropna(subset=["Survived"])
        for col in ["Age", "Fare", "Pclass", "SibSp", "Parch"]:
            if col in d.columns:
                d[col] = pd.to_numeric(d[col], errors="coerce")
        d["Survived"] = (
            pd.to_numeric(d["Survived"], errors="coerce").fillna(0).astype(int)
        )

        d["Title"] = (
            d["Name"]
            .str.extract(r"([A-Za-z]+)\.", expand=False)
            .replace(
                ["Capt", "Col", "Don", "Dr", "Major", "Rev", "Jonkheer", "Dona", "Mme"],
                "Rare",
            )
            .replace(["Countess", "Lady", "Sir"], "Royal")
            .replace({"Mlle": "Mr", "Ms": "Miss"})
        )
        d["Title"] = (
            d["Title"]
            .map({"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Royal": 5, "Rare": 6})
            .fillna(0)
            .astype(int)
        )
        d["gender"] = d["gender"].map({"male": 0, "female": 1})
        d["Age"] = d["Age"].fillna(-0.5)
        d["AgeGroup"] = (
            pd.cut(
                d["Age"],
                bins=[-1, 0, 5, 12, 18, 24, 35, 60, np.inf],
                labels=[0, 1, 2, 3, 4, 5, 6, 7],
            )
            .astype("Int64")
            .fillna(0)
            .astype(int)
        )
        d["Embarked"] = d["Embarked"].fillna("S").map({"S": 1, "C": 2, "Q": 3})
        d["FareBand"] = (
            pd.qcut(d["Fare"], 4, labels=[1, 2, 3, 4], duplicates="drop")
            .fillna(1)
            .astype(int)
        )
        _deck = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "T": 8}
        d["Deck"] = (
            d["Cabin"]
            .str.extract(r"^([A-Z])", expand=False)
            .map(_deck)
            .fillna(0)
            .astype(int)
        )
        return d.drop(
            columns=["Name", "Age", "Fare", "Ticket", "Cabin", "PassengerId"],
            errors="ignore",
        )

    # ─── BREAKDOWN: X별 생존율 ────────────────────────────────────────

    def _answer_breakdown(self, train_set: DataFrame, question: str) -> str:
        df = self._engineer(train_set)
        if "나이" in question or "연령" in question:
            group_col, header = "AgeGroup", "나이 그룹"
            label_fn = lambda idx: _AGE_LABELS.get(int(idx), str(idx))
        elif "성별" in question:
            group_col, header = "gender", "성별"
            label_fn = lambda idx: "여성" if int(idx) == 1 else "남성"
        elif "등급" in question or "좌석" in question:
            group_col, header = "Pclass", "좌석 등급"
            label_fn = lambda idx: f"{idx}등석"
        else:
            return self._answer_statistics(train_set)

        grouped = df.groupby(group_col)["Survived"].agg(["mean", "count"])
        lines = [f"{header}별 생존율:\n"]
        for idx, row in grouped.sort_index().iterrows():
            lines.append(
                f"  {label_fn(idx)}: {row['mean'] * 100:.1f}%  ({int(row['count'])}명)"
            )
        return "\n".join(lines)

    # ─── COUNT: 탑승 인원 ────────────────────────────────────────────

    async def _answer_count(self, train_set: DataFrame) -> str:
        total = await self.walter.get_total_count()
        survived_series = pd.to_numeric(
            train_set.get("Survived", pd.Series(dtype=float)), errors="coerce"
        ).dropna()
        survived = int(survived_series.sum())
        n = len(survived_series)
        rate = survived / n if n else 0
        return f"총 {total:,}명이 탑승했으며, 생존 기록이 있는 {n:,}명 중 {survived:,}명({rate:.1%})이 생존했습니다."

    # ─── STATISTICS: 상관관계 순위 ────────────────────────────────────

    def _answer_statistics(self, train_set: DataFrame) -> str:
        df = self._engineer(train_set)
        corr = df[_FEATURE_COLS + ["Survived"]].corr()["Survived"].drop("Survived")
        ranked = corr.abs().sort_values(ascending=False)
        lines = ["생존율(SurvivalStatus)에 영향을 미치는 요소 순위:\n"]
        for i, feat in enumerate(ranked.index, 1):
            coef = corr[feat]
            arrow = "▲" if coef > 0 else "▼"
            lines.append(f"  {i}. {_FEAT_LABELS.get(feat, feat)}: {coef:+.2f} {arrow}")
        return "\n".join(lines)

    # ─── SURVIVAL_PREDICT: 개인 생존 예측 ────────────────────────────

    def _extract_attrs(self, question: str) -> dict[str, Any]:
        attrs: dict[str, Any] = {}
        m = re.search(r"(\d+)\s*[세살]", question)
        if m:
            attrs["age"] = int(m.group(1))
        if any(w in question for w in ["여자", "여성", "여인", "female"]):
            attrs["gender"] = "female"
        elif any(w in question for w in ["남자", "남성", "male"]):
            attrs["gender"] = "male"
        m2 = re.search(r"([123])\s*등", question)
        if m2:
            attrs["pclass"] = int(m2.group(1))
        return attrs

    def _passenger_vector(self, attrs: dict[str, Any]) -> list[int]:
        age = attrs.get("age")
        g = 1 if attrs.get("gender") == "female" else 0
        pclass = attrs.get("pclass", 2)
        if age and age <= 12:
            title = 2 if g else 4
        else:
            title = 3 if g else 1
        if age is None:
            ag = 0
        elif age <= 5:
            ag = 1
        elif age <= 12:
            ag = 2
        elif age <= 18:
            ag = 3
        elif age <= 24:
            ag = 4
        elif age <= 35:
            ag = 5
        elif age <= 60:
            ag = 6
        else:
            ag = 7
        fare_band = {1: 4, 2: 2, 3: 1}.get(pclass, 2)
        return [pclass, g, 0, 0, 1, title, ag, fare_band, 0]

    def _answer_prediction(self, train_set: DataFrame, question: str) -> str:
        attrs = self._extract_attrs(question)
        if not attrs:
            return "예측을 위해 나이, 성별, 좌석 등급을 알려주세요.\n예: '33세 남자 2등석이라면 살 수 있었을까?'"

        df = self._engineer(train_set)
        X = df[_FEATURE_COLS].values
        y = df["Survived"].values
        clf = RandomForestClassifier(n_estimators=100, random_state=42)
        clf.fit(X, y)

        vec = np.array([self._passenger_vector(attrs)])
        pred = int(clf.predict(vec)[0])
        proba = float(clf.predict_proba(vec)[0][1])

        gender_label = "여성" if attrs.get("gender") == "female" else "남성"
        age_label = f"{attrs['age']}세 " if "age" in attrs else ""
        pclass_label = f"{attrs['pclass']}등석 " if "pclass" in attrs else ""
        result = (
            "생존했을 가능성이 높습니다"
            if pred == 1
            else "생존하지 못했을 가능성이 높습니다"
        )
        return f"{age_label}{gender_label} {pclass_label}승객은 {result}. (생존 확률: {proba * 100:.1f}%)"

    # ─── MODEL_TRAIN: 모델 성능 ───────────────────────────────────────

    def _answer_model(self, train_set: DataFrame) -> str:
        from sklearn.metrics import accuracy_score
        from sklearn.model_selection import train_test_split

        df = self._engineer(train_set)
        X = df[_FEATURE_COLS].values
        y = df["Survived"].values
        X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
        clf = RandomForestClassifier(n_estimators=100, random_state=42)
        clf.fit(X_tr, y_tr)
        acc = accuracy_score(y_te, clf.predict(X_te))
        return f"Random Forest 정확도 {acc * 100:.1f}%  (학습 {len(X_tr)}명 / 검증 {len(X_te)}명)"

    # ─── introduce_myself ─────────────────────────────────────────────

    async def introduce_myself(
        self, schema: SmithCaptainSchema
    ) -> SmithCaptainResponse:
        return await self.repository.introduce_myself(
            SmithCaptainQuery(id=schema.id, name=schema.name)
        )
