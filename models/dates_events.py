from sqlmodel import Field, Session, SQLModel, create_engine, select

class DatesEvents(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    event_name: str
    date: str
    subsidiarie_id: int = Field(default=None, foreign_key="subsidiarie.id")
