from typing import Optional

from sqlmodel import Field, SQLModel


class WorkersLogs(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    log_str: Optional[str] = Field(default=None)
    happened_at: Optional[str] = Field(default=None)
    happened_at_time: Optional[str] = Field(default=None)
    user_id: int = Field(default=None, foreign_key="user.id")
    subsidiarie_id: int = Field(default=None, foreign_key="subsidiarie.id")
