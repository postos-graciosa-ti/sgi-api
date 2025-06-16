from typing import Optional
from sqlmodel import SQLModel, Field

class ApplicantProcess(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    applicant_id: int = Field(index=True)

    exam: bool = False
    hr_interview: bool = False
    coordinator_interview: bool = False
    accounting_form: bool = False
    add_time_system: bool = False
    add_web_system: bool = False
    add_sgi_system: bool = False
