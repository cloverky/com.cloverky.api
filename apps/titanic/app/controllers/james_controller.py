from fastapi import FastAPI

from pathlib import Path
from titanic.app.services.jack_service import JackService
from titanic.app.repositories.walter_reader import WalterReader

app = FastAPI(title="Titanic (James)")
_DATA_DIR = Path(__file__).resolve().parent
_MODEL_PATH = _DATA_DIR.parent / "models" / "titanic_decision_tree.joblib"

class JamesController:
    def __init__(self):
        self.jack = JackService()
        self.w = WalterReader()


    def get_data(self):
        return self.w.get_data()

    def get_count(self):
        return self.w.get_count()    

    def get_count_survived(self):
        return self.w.get_count_survived()

    def get_count_not_survived(self):
        return self.w.get_count_not_survived()

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

