from typing import Optional

from sqlalchemy import Column, LargeBinary
from sqlmodel import Field, SQLModel


class ApplicantsDocs(SQLModel, table=True):
    __tablename__ = "applicantsdocs"

    id: Optional[int] = Field(default=None, primary_key=True)
    applicant_id: int = Field(foreign_key="applicants.id")
    resume: bytes = Field(sa_column=Column(LargeBinary))
    workcard: bytes = Field(sa_column=Column(LargeBinary))
