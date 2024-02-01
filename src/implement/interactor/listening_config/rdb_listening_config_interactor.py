from typing import Any, Optional
from bson import ObjectId
from pymongo import DeleteOne
from domain.exceptions import (
    DataListeningConfigNotFound,
)

from interfaces.usecase.listening_config_usecase import (
    StoreListeningConfigUseCase,
    UpdateListeningConfigUseCase,
    DeleteListeningConfigUseCase
)

from interfaces.usecase.listening_config_data import (
    StoreListeningConfigInputData,
    StoreListeningConfigOutData,
    UpdateListeningConfigInputData,
    UpdateListeningConfigOutData
)

from interfaces.usecase.result_data import (
    ResultData,
)


class RDBStoreListeningConfigInteractor(StoreListeningConfigUseCase):
    def handle(self, input_data: StoreListeningConfigInputData, db) -> StoreListeningConfigOutData:
        result = db.generate_configs.insert_one(input_data.dict())

        return StoreListeningConfigOutData(id=result.inserted_id)


class RDBUpdateListeningConfigInteractor(UpdateListeningConfigUseCase):
    def handle(self, config_id: str, input_data: UpdateListeningConfigInputData,
               db) -> UpdateListeningConfigOutData:
        result = db.generate_configs.find_one(ObjectId(config_id))
        if result is None:
            raise DataListeningConfigNotFound

        result.update(input_data.dict())

        return UpdateListeningConfigOutData(
            id=result['_id'],
            source=result['source'],
            source_config=result['source_config'],
            analyzer=result['analyzer'],
            analyzer_config=result['analyzer_config'],
            sink=result['sink'],
            sink_config=result['sink_config'],
            user_id=result['user_id']
        )


class RDBDeleteListeningConfigInteractor(DeleteListeningConfigUseCase):
    def handle(self, config_id: str, db) -> UpdateListeningConfigOutData:
        result = db.generate_configs.find_one(ObjectId(config_id))
        if result is None:
            raise DataListeningConfigNotFound

        db.generate_configs.delete_one({'_id': ObjectId(config_id)})

        return ResultData(ok=True)
