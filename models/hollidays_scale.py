from sqlmodel import Field, SQLModel


class HollidaysScale(SQLModel, table=True):
    __tablename__ = "hollidaysscale"

    id: int | None = Field(default=None, primary_key=True)
    subsidiarie_id: int = Field(default=None, foreign_key="subsidiarie.id", index=True)
    date: str
    working: str
    resting: str
