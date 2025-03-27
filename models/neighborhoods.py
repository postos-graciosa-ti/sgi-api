from sqlmodel import Field, SQLModel


class Neighborhoods(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    city_id: int = Field(default=None, foreign_key="cities.id")
