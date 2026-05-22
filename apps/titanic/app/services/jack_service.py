from titanic.app.repositories.walter_reader import WalterReader
from titanic.app.models.rose_model import RoseModel

_DEFAULT_TRAINING_MODEL_NAME = "DecisionTreeClassifier"


class JackService:

    def __init__(self):
        self.walter = WalterReader()
        self.rose = RoseModel()

    def get_training_model_name(self) -> str:
        tree = self.rose.decision_tree
        if tree is not None:
            return tree.__class__.__name__
        return _DEFAULT_TRAINING_MODEL_NAME

    def get_training_model_accuracy(self):
        tree = self.rose.decision_tree
        if tree is None:
            return None

        df = self.walter.get_full_data()
        if "Survived" not in df.columns:
            return None

        x = df.drop(columns=["Survived"])
        y = df["Survived"]

        try:
            score = tree.score(x, y)
            return round(float(score), 4)
        except Exception:
            return None

