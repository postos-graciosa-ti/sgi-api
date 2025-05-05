from datetime import time
from typing import List, Optional

from pydantic import conint
from sqlalchemy import JSON, Column, Time
from sqlmodel import Field, Session, SQLModel, create_engine, select


class TicketsComments(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ticket_id: int = Field(default=None, foreign_key="tickets.id")
    comentator_id: int = Field(default=None, foreign_key="user.id")
    comment: str = Field(default=None, nullable=True)
