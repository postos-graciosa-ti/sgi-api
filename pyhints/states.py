from pydantic import BaseModel


class GetStatesOutput(BaseModel):
    label: str
    value: int
