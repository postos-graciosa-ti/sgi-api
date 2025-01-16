from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import date

class Scale(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    worker_id: int = Field(default=None, foreign_key="workers.id")
    worker_turn_id: int = Field(index=True)
    worker_function_id: int = Field(index=True)
    subsidiarie_id: int = Field(default=None, foreign_key="subsidiarie.id")
    days_on: str = Field(default="[]")
    days_off: str = Field(default="[]")
    ilegal_dates: str = Field(default="[]")
    need_alert: bool = Field(default=False)
    proportion: str
