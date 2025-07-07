from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, LargeBinary


class WorkersCourses(SQLModel, table=True):
    __tablename__ = "workerscourses"

    id: Optional[int] = Field(default=None, primary_key=True)
    worker_id: int
    file: bytes = Field(sa_column=Column(LargeBinary))
    date_file: str  # ou date_file: datetime se quiser converter para datetime
    is_payed: bool
