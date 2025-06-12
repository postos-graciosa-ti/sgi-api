from datetime import datetime

from sqlmodel import Field, SQLModel


class ApplicantsAppointments(SQLModel, table=True):
    __tablename__ = "applicantsappointments"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    date: datetime
