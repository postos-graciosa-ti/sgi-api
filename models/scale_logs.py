from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class ScaleLogs(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id")
    worker_id: int = Field(default=None, foreign_key="workers.id")
    inserted_at: str
    at_time: str
