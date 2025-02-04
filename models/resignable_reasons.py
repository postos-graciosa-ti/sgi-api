from sqlmodel import Field, SQLModel


class ResignableReasons(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str = Field(index=True)
