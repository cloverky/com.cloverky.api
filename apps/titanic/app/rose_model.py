from pathlib import Path

try:
    import joblib
except ModuleNotFoundError:
    joblib = None

_DATA_DIR = Path(__file__).resolve().parent
_MODEL_PATH = _DATA_DIR / "titanic_decision_tree.joblib"


class RoseModel:
    def __init__(self) -> None:
        self.decision_tree = (
            joblib.load(_MODEL_PATH)
            if joblib is not None and _MODEL_PATH.exists()
            else None
        )
