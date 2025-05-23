from sqlmodel import Field, SQLModel


class ApplicantsExams(SQLModel, table=True):
    __tablename__ = "applicantsexams"

    id: int | None = Field(default=None, primary_key=True)
    applicant_id: int
    exam_label: str
    status: str
    responses: str = Field(default="[]")
    asijfvhzdiu: str
    