from sqlmodel import Field, Session, SQLModel, create_engine, select

class Applicants(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(default=None, nullable=True)