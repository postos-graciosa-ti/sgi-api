from sqlmodel import Field, Session, SQLModel, create_engine, select


class States(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    sail: str
