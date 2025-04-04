from sqlmodel import Field, Session, SQLModel, create_engine, select

class Subsidiarie(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    adress: str = Field(index=True)
    phone: str = Field(index=True)
    email: str = Field(index=True)