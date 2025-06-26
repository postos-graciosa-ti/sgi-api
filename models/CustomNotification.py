from sqlmodel import Field, SQLModel
from datetime import date


class CustomNotification(SQLModel, table=True):
    __tablename__ = "customnotification"

    id: int | None = Field(default=None, primary_key=True)
    
    user_id: int = Field(default=None, foreign_key="user.id", index=True)
    date: date
    title: str
    description: str