from sqlmodel import Field, SQLModel


class WorkersParents(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    worker_id: int = Field(default=None, foreign_key="workers.id")
    parent_type_id: int = Field(default=None, foreign_key="parentstype.id")
    name: str = Field(index=True)
    cpf: str = Field(default=None, nullable=True)
    birthdate: str = Field(default=None, nullable=True)
    books: int = Field(default=None, nullable=True)
    papers: int = Field(default=None, nullable=True)
