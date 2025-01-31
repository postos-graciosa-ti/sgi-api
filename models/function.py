from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select


class Function(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str = Field(index=True)
    ideal_quantity: Optional[int] = Field(default=None)
    subsidiarie_id: int = Field(default=None, foreign_key="subsidiarie.id")
