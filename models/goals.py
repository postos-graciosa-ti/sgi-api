from sqlmodel import Field, SQLModel


class Goals(SQLModel, table=True):
    __tablename__ = "goals"

    id: int = Field(default=None, primary_key=True)
    subsidiarie_id: int = Field(default=None, foreign_key="subsidiarie.id", index=True)
    month: str
    year: str
    ligeirinho: str = Field(default="[]")
