from datetime import time
from typing import List, Optional

from pydantic import conint
from sqlalchemy import JSON, Column, Time
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Tickets(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    requesting_id: int = Field(default=None, foreign_key="user.id")
    responsibles_ids: List[int] = Field(default_factory=list, sa_column=Column(JSON))
    service: int = Field(default=None, foreign_key="service.id")
    description: str = Field(default=None, nullable=True)
    is_open: bool | None = Field(default=None, nullable=True)
    opened_at: str = Field(default=None, nullable=True)
    closed_at: str = Field(default=None, nullable=True)
