from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import date

class Scale(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    date: str = Field(default="[]")
    worker_id: Optional[int] = Field(default=None, foreign_key="workers.id")
    month_id: Optional[int] = Field(default=None, foreign_key="month.id")
