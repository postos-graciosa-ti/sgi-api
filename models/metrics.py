from sqlmodel import Field, SQLModel


class Metrics(SQLModel, table=True):
    __tablename__ = "metrics"

    id: int = Field(default=None, primary_key=True)

    year_month: str

    ligeirinho: str
