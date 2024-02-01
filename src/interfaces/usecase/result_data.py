from pydantic import BaseModel


class ResultData(BaseModel):
    ok: bool
