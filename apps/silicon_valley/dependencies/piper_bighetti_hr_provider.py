from silicon_valley.adapter.outbound.repositories.piper_bighetti_hr_repository import (
    BighettiHrPgRepository,
)
from silicon_valley.app.ports.input.piper_bighetti_hr_use_case import BighettiHrUseCase
from silicon_valley.app.use_cases.piper_bighetti_hr_interactor import (
    BighettiHrInteractor,
)


def get_bighetti_hr_use_case() -> BighettiHrUseCase:
    return BighettiHrInteractor(repository=BighettiHrPgRepository())
