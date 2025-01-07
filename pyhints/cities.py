from pydantic import BaseModel


class GetCitiesOutput(BaseModel):
    label: str
    value: int
