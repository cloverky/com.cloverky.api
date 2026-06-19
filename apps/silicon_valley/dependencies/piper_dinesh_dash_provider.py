from silicon_valley.adapter.outbound.repositories.piper_dinesh_dash_repository import DineshDashPgRepository
from silicon_valley.app.ports.input.piper_dinesh_dash_use_case import DineshDashUseCase
from silicon_valley.app.use_cases.piper_dinesh_dash_interactor import DineshDashInteractor


def get_dinesh_dash_use_case() -> DineshDashUseCase:
    return DineshDashInteractor(repository=DineshDashPgRepository())
