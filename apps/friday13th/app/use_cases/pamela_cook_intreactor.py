from friday13th.app.ports.output.pamela_cook_repository import PamelaCookRepository

class PamelaCookInteractor(PamelaCookUseCase):
    def get_pamela_cook(self) -> str:
        return "Hello, Pamela Cook!"