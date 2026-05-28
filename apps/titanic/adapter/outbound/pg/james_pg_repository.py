import logging
from typing import Dict, List

from sqlalchemy import delete
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.orm.titanic_passenger_model import TitanicPassengerModel
from titanic.app.ports.output.james_repository import JamesRepository


logger = logging.getLogger(__name__)


class JamesPgRepository(JamesRepository):
    """JamesRepository 출력 포트 — Neon Postgres 어댑터."""

    async def save_rows(
        self,
        db: AsyncSession,
        rows: List[Dict[str, str]],
    ) -> Dict[str, object]:
        if not rows:
            logger.info("[JamesPg] 저장할 row 없음")
            return {"count": 0, "rows": []}

        prepared = [self._normalize_row(row) for row in rows]
        logger.info("[JamesPg] Neon DB 저장 시작 — rows=%d", len(prepared))
        saved: list[dict[str, object]] = []

        try:
            await db.execute(delete(TitanicPassengerModel))
            logger.info("[JamesPg] 기존 titanic_passengers 전체 삭제 완료")

            for row in prepared:
                entity = TitanicPassengerModel(
                    passenger_id=self._to_int(row["PassengerId"]),
                    survived=self._to_int(row["Survived"]),
                    pclass=self._to_int(row["Pclass"]),
                    name=row["Name"].strip(),
                    gender=(row.get("Sex") or row.get("gender") or "").strip(),
                    age=self._to_optional_float(row.get("Age")),
                    sibsp=self._to_int(row["SibSp"]),
                    parch=self._to_int(row["Parch"]),
                    ticket=row["Ticket"].strip(),
                    fare=self._to_float(row["Fare"]),
                    cabin=self._optional_str(row.get("Cabin")),
                    embarked=self._optional_str(row.get("Embarked")),
                )
                db.add(entity)
                await db.flush()
                saved.append(
                    {
                        "id": entity.id,
                        "passenger_id": entity.passenger_id,
                        "name": entity.name,
                        "gender": entity.gender,
                    },
                )

            await db.commit()
        except OperationalError as exc:
            await db.rollback()
            logger.exception("[JamesPg] Neon DB 연결 오류 — 롤백 수행")
            raise RuntimeError("Neon DB 연결이 일시적으로 끊어졌습니다. 잠시 후 다시 시도해 주세요.") from exc
        except Exception:
            await db.rollback()
            logger.exception("[JamesPg] 저장 실패 — 롤백 수행")
            raise
        logger.info("[JamesPg] Neon DB 저장 완료 — committed=%d", len(saved))
        return {"count": len(saved), "rows": saved}

    @staticmethod
    def _normalize_row(row: Dict[str, str]) -> Dict[str, str]:
        normalized = dict(row)
        gender = normalized.pop("gender", None) or normalized.get("Sex", "")
        if gender and "Sex" not in normalized:
            normalized["Sex"] = gender.strip()
        return normalized

    @staticmethod
    def _optional_str(value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned or None

    @staticmethod
    def _to_int(value: str) -> int:
        return int((value or "0").strip())

    @staticmethod
    def _to_float(value: str) -> float:
        return float((value or "0").strip())

    @staticmethod
    def _to_optional_float(value: str | None) -> float | None:
        if value is None:
            return None
        cleaned = value.strip()
        if not cleaned:
            return None
        return float(cleaned)
