from friday13th.app.ports.output.jason_mask_repository import JasonMaskRepository

class JasonMaskInteractor(JasonMaskUseCase):
    def get_jason_mask(self) -> str:
        return "Hello, Jason Mask!"