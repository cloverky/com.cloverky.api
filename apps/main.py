from fastapi import FastAPI
from db_health_adapter import DbHealthPort, SqlAlchemyAsyncDbHealthAdapter
from database import AsyncSessionLocal, DB_UNAVAILABLE_DETAIL
from doro.app.doro_director import DoroDirector
from titanic.app.james_controller import JamesController

app = FastAPI(title="cloverky Main Page")

_db_health: DbHealthPort = SqlAlchemyAsyncDbHealthAdapter(
    AsyncSessionLocal,
    DB_UNAVAILABLE_DETAIL,
)


@app.get("/db-check")
async def check_db() -> dict:
    return await _db_health.check()

@app.get("/")
def read_root():
    return {"message": "FAST API 메인 페이지 ", "docs": "/docs"}


@app.get("/titanic/data")
def read_titanic_data():
    james = JamesController()
    df = james.get_data()

    return df.to_dict(orient="records")

@app.get("/titanic/count")
def read_titanic_count():
    james = JamesController()
    count = james.get_count()

    return {"count": count}

@app.get("/titanic/tree")
def read_titanic_tree():
    james = JamesController()
    tree = james.has_decision_tree_model()

    return {"tree": tree}

@app.get("/titanic/count/survived")
def read_titanic_count_survived():
    james = JamesController()
    count = james.get_count_survived()

    return {"count": count}

@app.get("/titanic/count/not_survived")
def read_titanic_count_not_survived():
    james = JamesController()
    count = james.get_count_not_survived()

    return {"count": count}


@app.get("/titanic/model")
def read_titanic_model():
    james = JamesController()
    model_name = james.get_training_model_name()
    accuracy = james.get_training_model_accuracy()

    return {"model": model_name, "accuracy": accuracy}
    
@app.get("/doro/data")
def read_doro_data():
    doro_director = DoroDirector()
    df = doro_director.get_data()

    return df.to_dict(orient="records")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

    