from typing import Optional

from sqlmodel import Field, SQLModel


class WorkersLogsDelete(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    deleted_at: Optional[str] = Field(default=None)
    deleted_at_time: Optional[str] = Field(default=None)
    subsidiarie_id: int = Field(default=None, foreign_key="subsidiarie.id")
    user_id: int = Field(default=None, foreign_key="user.id")
    worker_id: int = Field(default=None, foreign_key="workers.id")
