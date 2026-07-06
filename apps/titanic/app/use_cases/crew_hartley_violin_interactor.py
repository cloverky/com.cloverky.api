from __future__ import annotations

import io

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from titanic.adapter.inbound.api.schemas.crew_hartley_violin_schema import (
    HartleyViolinSchema,
)
from titanic.app.dtos.crew_hartley_violin_dto import (
    HartleyViolinQuery,
    HartleyViolinResponse,
)
from titanic.app.ports.input.crew_hartley_violin_use_case import HartleyViolinUseCase
from titanic.app.ports.output.crew_hartley_violin_port import HartleyViolinPort


class HartleyViolinInteractor(HartleyViolinUseCase):
    def __init__(self, repository: HartleyViolinPort):
        self.repository = repository

    async def get_correlation_heatmap(self, df: pd.DataFrame) -> bytes:
        df = df.copy()
        if "Cabin" in df.columns:
            _deck = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "T": 8}
            df["Deck"] = (
                df["Cabin"]
                .str.extract(r"^([A-Z])", expand=False)
                .map(_deck)
                .fillna(0)
                .astype(int)
            )
            df = df.drop(columns=["Cabin"])

        numeric_df = df.select_dtypes(include=["number"])
        numeric_df = numeric_df.rename(
            columns={
                "Survived": "SurvivalStatus",
                "Pclass": "PClass",
                "Gender": "Gender",
                "gender": "Gender",
                "AgeGroup": "Age",
                "SibSp": "SibSp",
                "Parch": "Parch",
                "Embarked": "Embarkation",
                "Title": "Title",
                "FareBand": "Fare",
                "Deck": "Cabin",
            }
        )
        corr = numeric_df.corr()

        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
        ax.set_title("Titanic Feature Correlation")

        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        plt.close(fig)

        return buf.getvalue()

    async def introduce_myself(
        self, schema: HartleyViolinSchema
    ) -> HartleyViolinResponse:
        return await self.repository.introduce_myself(
            HartleyViolinQuery(id=schema.id, name=schema.name)
        )
