from bson import ObjectId
from interfaces.usecase.listening_config_usecase import (
    StoreListeningConfigUseCase,
    UpdateListeningConfigUseCase,
    DeleteListeningConfigUseCase,
)

from interfaces.usecase.listening_config_data import (
    StoreListeningConfigInputData,
    StoreListeningConfigOutData,
    UpdateListeningConfigInputData,
    UpdateListeningConfigOutData,
)
from schema.listening_config import (
    Analyzer,
    AnalyzerConfig,
    Source,
    SourceConfig,
    Sink,
    SinkConfig,
)

from interfaces.usecase.result_data import (
    ResultData,
)

class ConfigService():
    def __init__(
            self,
            store_listening_config_use_case: StoreListeningConfigUseCase = None,
            update_listening_config_use_case: UpdateListeningConfigUseCase = None,
            delete_listening_config_use_case: DeleteListeningConfigUseCase = None,

    ):
        self.store_listening_config_use_case = store_listening_config_use_case
        self.update_listening_config_use_case = update_listening_config_use_case
        self.delete_listening_config_use_case = delete_listening_config_use_case

    def store_listening_config(
            self,
            user_id: str,
            source: Source,
            source_config: SourceConfig,
            analyzer: Analyzer,
            analyzer_config: SourceConfig,
            sink: Sink,
            sink_config: SinkConfig,
            db
    ) -> StoreListeningConfigOutData:
        input = StoreListeningConfigInputData(source=source, source_config=source_config, analyzer=analyzer,
                                              analyzer_config=analyzer_config, sink=sink,
                                              sink_config=sink_config,
                                              user_id=user_id)

        return self.store_listening_config_use_case.handle(input, db=db)

    def update_listening_config(
            self,
            config_id: str,
            source: Source,
            source_config: SourceConfig,
            analyzer: Analyzer,
            analyzer_config: SourceConfig,
            sink: Sink,
            sink_config: SinkConfig,
            db
    ) -> UpdateListeningConfigOutData:
        input = UpdateListeningConfigInputData(source=source, source_config=source_config,
                                               analyzer=analyzer,
                                               analyzer_config=analyzer_config, sink=sink,
                                               sink_config=sink_config)

        return self.update_listening_config_use_case.handle(config_id, input, db=db)

    def delete_listening_config(self, config_id: str, db) -> ResultData:
        return self.delete_listening_config_use_case.handle(config_id, db=db)
