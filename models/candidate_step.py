from sqlmodel import Field, Session, SQLModel, create_engine, select

class Candidate_Step(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    status: int = Field(foreign_key="candidatestatus.id", nullable=True)
    