from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from titanic.app.controllers.james_controller import JamesController

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
