from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select


class IndicatorsCriteria(SQLModel, table=True):
    __tablename__ = "indicatorscriteria"
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
