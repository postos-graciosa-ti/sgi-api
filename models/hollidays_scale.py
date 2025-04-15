from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select


class HollidaysScale(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    date: str = Field(default=None)
    worker_id: int = Field(foreign_key="workers.id")
    worker_turn_id: int = Field(index=True)
    worker_function_id: int = Field(index=True)
    subsidiarie_id: int = Field(default=None, foreign_key="subsidiarie.id")
