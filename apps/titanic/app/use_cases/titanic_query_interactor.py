from __future__ import annotations

from typing import Any

from titanic.app.ports.input.titanic_query_use_case import TitanicQueryUseCase
from titanic.app.use_cases._james_command import JamesController


class TitanicQueryInteractor(TitanicQueryUseCase):

    def __init__(self, controller: JamesController | None = None) -> None:
        self._controller = controller or JamesController()

    def get_tree(self) -> dict[str, Any]:
        return {"tree": self._controller.has_decision_tree_model()}

    def get_model(self) -> dict[str, Any]:
        return self._controller.get_model_name_and_accuracy()
