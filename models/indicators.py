from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Indicators(SQLModel, table=True):
    __tablename__ = "indicators"

    id: int = Field(default=None, primary_key=True)
    month: str
    criteria_id: int
    workers_ids: str
    note: str


class PostIndicatorsByMonthAndCriteria(BaseModel):
    month: str
    criteria_id: int
