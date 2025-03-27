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
    esocial: str = Field(default=None, nullable=True)
    teste: str = Field(default=None, nullable=True)

    gender_id: int = Field(default=None, nullable=True, foreign_key="genders.id")
    civil_status_id: int = Field(
        default=None, nullable=True, foreign_key="civilstatus.id"
    )

    street: str = Field(default=None, nullable=True)
    street_number: str = Field(default=None, nullable=True)
    street_complement: str = Field(default=None, nullable=True)
    neighborhood_id: int = Field(
        default=None, nullable=True, foreign_key="neighborhoods.id"
    )
    cep: str = Field(default=None, nullable=True)
    city: str = Field(default=None, nullable=True)
    state: str = Field(default=None, nullable=True)

    phone: str = Field(default=None, nullable=True)
    mobile: str = Field(default=None, nullable=True)
    email: str = Field(default=None, nullable=True)
    ethnicity_id: int = Field(default=None, nullable=True, foreign_key="ethnicity.id")

    birthdate: str = Field(default=None, nullable=True)
    birthcity: str = Field(default=None, nullable=True)
    birthstate: str = Field(default=None, nullable=True)
    nationality: str = Field(default=None, nullable=True)

    fathername: str = Field(default=None, nullable=True)
    mothername: str = Field(default=None, nullable=True)
    