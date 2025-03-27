from sqlmodel import Field, Session, SQLModel, create_engine


class Country(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
