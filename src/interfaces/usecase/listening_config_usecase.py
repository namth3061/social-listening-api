from abc import ABCMeta
from interfaces.usecase.listening_config_data import (
    StoreListeningConfigInputData,
    StoreListeningConfigOutData,
    UpdateListeningConfigInputData,
    UpdateListeningConfigOutData,
)

from interfaces.usecase.result_data import (
    ResultData,
)


class StoreListeningConfigUseCase(metaclass=ABCMeta):
    def handle(self, input_data: StoreListeningConfigInputData, db) -> StoreListeningConfigOutData:
        raise NotImplementedError


class UpdateListeningConfigUseCase(metaclass=ABCMeta):
    def handle(self, config_id: str, input_data: UpdateListeningConfigInputData, db) -> UpdateListeningConfigOutData:
        raise NotImplementedError


class DeleteListeningConfigUseCase(metaclass=ABCMeta):
    def handle(self, config_id: str, db) -> ResultData:
        raise NotImplementedError
