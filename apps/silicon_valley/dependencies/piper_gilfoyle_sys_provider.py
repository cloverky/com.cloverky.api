from silicon_valley.adapter.outbound.repositories.piper_gilfoyle_sys_repository import (
    GilfoyleSysPgRepository,
)
from silicon_valley.app.ports.input.piper_gilfoyle_sys_use_case import (
    GilfoyleSysUseCase,
)
from silicon_valley.app.use_cases.piper_gilfoyle_sys_interactor import (
    GilfoyleSysInteractor,
)


def get_gilfoyle_sys_use_case() -> GilfoyleSysUseCase:
    return GilfoyleSysInteractor(repository=GilfoyleSysPgRepository())
