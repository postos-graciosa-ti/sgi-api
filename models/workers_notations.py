from sqlmodel import Field, SQLModel


class WorkersNotations(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    notation: str = Field(index=True, nullable=True)
    worker_id: int = Field(default=None, foreign_key="workers.id")
