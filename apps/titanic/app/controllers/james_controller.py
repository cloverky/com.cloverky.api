from fastapi import FastAPI

from pathlib import Path
from titanic.app.use_cases.jack_service import JackService

app = FastAPI(title="Titanic (James)")
_DATA_DIR = Path(__file__).resolve().parent
_MODEL_PATH = _DATA_DIR.parent / "models" / "titanic_decision_tree.joblib"

class JamesController:
    def __init__(self):
        self.jack = JackService()

    def has_decision_tree_model(self):
        return _MODEL_PATH.exists()

    def get_training_model_name(self):
        return self.jack.get_training_model_name()

    def get_training_model_accuracy(self):
        return self.jack.get_training_model_accuracy()

    def get_model_name_and_accuracy(self) -> dict:
        return {
            "model": self.get_training_model_name(),
            "accuracy": self.get_training_model_accuracy(),
        }

