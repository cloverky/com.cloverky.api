from typing import Any, Dict

from titanic.app.dtos.passenger_schema import TitanicPassengerSchema


class CaledonValidation:
    """Rose's fiancé Caledon Hockley checking/validating the passenger list."""

    @staticmethod
    def validate_passenger(data: Dict[str, Any]) -> TitanicPassengerSchema:
        return TitanicPassengerSchema(**data)
