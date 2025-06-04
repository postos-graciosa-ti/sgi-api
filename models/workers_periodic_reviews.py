from sqlmodel import Field, SQLModel


class WorkersPeriodicReviews(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    worker_id: int | None = Field(default=None, index=True, foreign_key="workers.id")
    label: str
    date: str
    answers: str
