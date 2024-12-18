from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import date

class Scale(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    date: date
    subsidiarie_id: int = Field(default=None, foreign_key="subsidiarie.id")
    workers_on: str = Field(default="[]")
    workers_off: str = Field(default="[]")
    