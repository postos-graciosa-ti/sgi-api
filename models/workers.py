from typing import Optional

from sqlmodel import Field, SQLModel


class Workers(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    function_id: int = Field(default=None, foreign_key="function.id")
    subsidiarie_id: int = Field(default=None, foreign_key="subsidiarie.id")
    is_active: bool = Field(default=True)
    turn_id: int = Field(default=None, foreign_key="turn.id")
    cost_center_id: int = Field(default=None, foreign_key="costcenter.id")
    department_id: int = Field(default=None, foreign_key="department.id")
    admission_date: str = Field(index=True)
    resignation_date: str = Field(index=True)
    resignation_reason_id: Optional[int] = Field(
        default=None, foreign_key="resignablereasons.id", nullable=True
    )
    sales_code: str = Field(default=None, nullable=True)
    enrolment: str = Field(default=None, nullable=True)
    picture: str = Field(default=None, nullable=True)
    timecode: str = Field(default=None, nullable=True)
    first_review_date: str = Field(default=None, nullable=True)
    second_review_date: str = Field(default=None, nullable=True)
