from sqlmodel import Field, SQLModel


class WorkersFiles(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    worker_id: int = Field(default=None, foreign_key="workers.id")
    filename: str
    content: bytes
    size: int
