from titanic.app.models.rose_model import RoseModel

_DEFAULT_TRAINING_MODEL_NAME = "DecisionTreeClassifier"


class JackService:

    def __init__(self):
        self.rose = RoseModel()

    def get_training_model_name(self) -> str:
        tree = self.rose.decision_tree
        if tree is not None:
            return tree.__class__.__name__
        return _DEFAULT_TRAINING_MODEL_NAME

    def get_training_model_accuracy(self):
        return None
