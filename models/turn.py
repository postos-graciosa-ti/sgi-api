from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy import Time
from datetime import time

class Turn(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    start_time: time = Field(sa_column=Field(Time))
    start_interval_time: time = Field(sa_column=Time())
    end_time: time = Field(sa_column=Time())
    end_interval_time: time = Field(sa_column=Time())
    subsidiarie_id: int = Field(default=None, foreign_key="subsidiarie.id")
    week: str = Field(default=None, nullable=True)
