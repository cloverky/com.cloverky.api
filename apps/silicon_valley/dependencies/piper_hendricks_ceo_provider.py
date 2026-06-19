from silicon_valley.adapter.outbound.repositories.piper_hendricks_ceo_repository import HendricksCeoPgRepository
from silicon_valley.app.ports.input.piper_hendricks_ceo_use_case import HendricksCeoUseCase
from silicon_valley.app.use_cases.piper_hendricks_ceo_interactor import HendricksCeoInteractor


def get_hendricks_ceo_use_case() -> HendricksCeoUseCase:
    return HendricksCeoInteractor(repository=HendricksCeoPgRepository())
