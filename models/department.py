from sqlmodel import Field, Session, SQLModel, create_engine, select

class Department(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    description: str
