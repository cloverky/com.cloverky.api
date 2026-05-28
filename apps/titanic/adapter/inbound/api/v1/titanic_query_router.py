from pathlib import Path

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

try:
    from titanic.app.use_cases._james_command import JamesController
except ModuleNotFoundError:
    _DATA_DIR = Path(__file__).resolve().parents[4] / "app"
    _MODEL_PATH = _DATA_DIR.parent / "models" / "titanic_decision_tree.joblib"

    class JamesController:  # type: ignore[no-redef]
        def has_decision_tree_model(self):
            return _MODEL_PATH.exists()

        def get_model_name_and_accuracy(self) -> dict:
            return {"model": "DecisionTreeClassifier", "accuracy": None}

titanic_router = APIRouter(prefix="/titanic", tags=["titanic"])


@titanic_router.get("/tree")
def read_titanic_tree():
    james = JamesController()
    tree = james.has_decision_tree_model()
    return {"tree": tree}


@titanic_router.get("/model")
def read_titanic_model():
    controller = JamesController()
    model_name = controller.get_model_name_and_accuracy()
    return JSONResponse(content=jsonable_encoder(model_name))
