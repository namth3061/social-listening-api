from typing import Annotated, Any
from bson import ObjectId
from pydantic_core import core_schema
from pydantic import BaseModel
from pydantic.json_schema import JsonSchemaValue
from schema.listening_config import (
    Analyzer,
    AnalyzerConfig,
    Source,
    SourceConfig,
    Sink,
    SinkConfig,
)


class StoreListeningConfigInputData(BaseModel):
    source: Source
    source_config: SourceConfig
    analyzer: Analyzer
    analyzer_config: AnalyzerConfig
    sink: Sink
    sink_config: SinkConfig
    user_id: str


class UpdateListeningConfigInputData(BaseModel):
    source: Source
    source_config: SourceConfig
    analyzer: Analyzer
    analyzer_config: AnalyzerConfig
    sink: Sink
    sink_config: SinkConfig


class ObjectIdPydanticAnnotation:
    @classmethod
    def validate_object_id(cls, v: Any, handler) -> ObjectId:
        if isinstance(v, ObjectId):
            return v

        s = handler(v)
        if ObjectId.is_valid(s):
            return ObjectId(s)
        else:
            raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, _handler) -> core_schema.CoreSchema:
        assert source_type is ObjectId
        return core_schema.no_info_wrap_validator_function(
            cls.validate_object_id,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema, handler) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


class StoreListeningConfigOutData(BaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]


class UpdateListeningConfigOutData(BaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    source: object
    source_config: object
    analyzer: object
    analyzer_config: object
    sink: object
    sink_config: object
    user_id: str
