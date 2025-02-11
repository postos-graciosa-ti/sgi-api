from typing import Optional

from sqlmodel import Field, SQLModel


class TurnsLogs(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    happened_at: Optional[str] = Field(default=None)
    happened_at_time: Optional[str] = Field(default=None)
    http_method: int
    subsidiarie_id: int = Field(default=None, foreign_key="subsidiarie.id")
    user_id: int = Field(default=None, foreign_key="user.id")
    turn_id: int = Field(default=None, foreign_key="workers.id")
