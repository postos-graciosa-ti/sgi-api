from typing import Optional

from sqlmodel import Field, SQLModel


class WorkersSecondReview(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    worker_id: int
    personal_presentation: str = Field(default=None, nullable=True)
    productivity: str = Field(default=None, nullable=True)
    knowledge: str = Field(default=None, nullable=True)
    cooperation: str = Field(default=None, nullable=True)
    initiative: str = Field(default=None, nullable=True)
    interpersonal_relationships: str = Field(default=None, nullable=True)
    learning: str = Field(default=None, nullable=True)
    hierarchy: str = Field(default=None, nullable=True)
    punctuality: str = Field(default=None, nullable=True)
    attendance: str = Field(default=None, nullable=True)
    approved: str = Field(default=None, nullable=True)
