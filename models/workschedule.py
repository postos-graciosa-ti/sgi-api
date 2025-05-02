from datetime import date
from typing import List, Optional

from pydantic import conint
from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


class Workschedule(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    subsidiarie_id: int = Field(default=None, index=True, foreign_key="subsidiarie.id")
    worker_id: int = Field(default=None, index=True, foreign_key="workers.id")
    turn_id: int = Field(default=None, index=True, foreign_key="turn.id")
    month: str
    year: str
    days_on: List[int] = Field(default_factory=list, sa_column=Column(JSON))
    days_off: List[int] = Field(default_factory=list, sa_column=Column(JSON))
