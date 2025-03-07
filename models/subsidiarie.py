from sqlmodel import Field, Session, SQLModel, create_engine, select

class Subsidiarie(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cnpj: str = Field(default=None, nullable=True)
    name: str = Field(index=True)
    adress: str = Field(index=True)
    phone: str = Field(index=True)
    email: str = Field(index=True)
    coordinator: int = Field(default=None, foreign_key="user.id")
    manager: int = Field(default=None, nullable=True, foreign_key="user.id")
