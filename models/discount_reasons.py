from sqlmodel import Field, SQLModel


class DiscountReasons(SQLModel, table=True):
    __tablename__ = "discountreasons"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
