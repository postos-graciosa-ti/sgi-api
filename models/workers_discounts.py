from sqlmodel import Field, SQLModel


class WorkersDiscounts(SQLModel, table=True):
    __tablename__ = "workersdiscounts"

    id: int | None = Field(default=None, primary_key=True)
    worker_id: int = Field(foreign_key="workers.id")
    discount_reason_id: int = Field(foreign_key="workers.id")
    value: str
