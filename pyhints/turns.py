from pydantic import BaseModel


class PutTurn(BaseModel):
    name: str
    start_time: str
    start_interval_time: str
    end_time: str
    end_interval_time: str
