from sqlmodel import Field, SQLModel


class ApplicantsExams(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    applicant_id: int
    exam_label: str
    responses: str = Field(default="[]")
