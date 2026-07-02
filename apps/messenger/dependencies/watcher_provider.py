from fastapi import Depends

from messenger.app.ports.input.receive_use_case import ReceiveUseCase
from messenger.app.ports.input.watcher_use_case import WatcherUseCase
from messenger.app.use_cases.watcher_interactor import WatcherInteractor
from messenger.dependencies.receive_provider import get_receive_use_case


def get_watcher_use_case(
    receive: ReceiveUseCase = Depends(get_receive_use_case),
) -> WatcherUseCase:
    return WatcherInteractor(receive=receive)
