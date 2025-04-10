from sqlmodel import Field, SQLModel


class HierarchyStructure(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
