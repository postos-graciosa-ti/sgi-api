from typing import Optional
from sqlmodel import Field, SQLModel


class Workers(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Basic Information
    name: str = Field(index=True)
    function_id: int = Field(default=None, foreign_key="function.id")
    subsidiarie_id: int = Field(default=None, foreign_key="subsidiarie.id")
    is_active: bool = Field(default=True)
    turn_id: int = Field(default=None, foreign_key="turn.id")
    cost_center_id: int = Field(default=None, foreign_key="costcenter.id")
    department_id: int = Field(default=None, foreign_key="department.id")
    admission_date: str
    resignation_date: Optional[str] = Field(default=None, nullable=True)
    resignation_reason_id: Optional[int] = Field(
        default=None, foreign_key="resignablereasons.id", nullable=True
    )
    sales_code: Optional[str] = Field(default=None, nullable=True)
    enrolment: Optional[str] = Field(default=None, nullable=True)
    picture: Optional[str] = Field(default=None, nullable=True)
    timecode: Optional[str] = Field(default=None, nullable=True)
    first_review_date: Optional[str] = Field(default=None, nullable=True)
    second_review_date: Optional[str] = Field(default=None, nullable=True)
    esocial: Optional[str] = Field(default=None, nullable=True)

    # Personal Information
    gender_id: Optional[int] = Field(
        default=None, foreign_key="genders.id", nullable=True
    )
    civil_status: Optional[str] = Field(default=None, nullable=True)
    ethnicity_id: Optional[int] = Field(
        default=None, foreign_key="ethnicity.id", nullable=True
    )
    birthdate: Optional[str] = Field(default=None, nullable=True)
    nationality: Optional[str] = Field(default=None, nullable=True)
    birthstate_id: Optional[int] = Field(
        default=None, foreign_key="states.id", nullable=True
    )
    birthcity_id: Optional[int] = Field(
        default=None, foreign_key="cities.id", nullable=True
    )
    mothername: Optional[str] = Field(default=None, nullable=True)
    fathername: Optional[str] = Field(default=None, nullable=True)
    children: Optional[bool] = Field(default=None, nullable=True)

    # Contact Information
    phone: Optional[str] = Field(default=None, nullable=True)
    mobile: Optional[str] = Field(default=None, nullable=True)
    email: Optional[str] = Field(default=None, nullable=True)

    # Address Information
    state_id: Optional[int] = Field(
        default=None, foreign_key="states.id", nullable=True
    )
    city_id: Optional[int] = Field(default=None, foreign_key="cities.id", nullable=True)
    neighborhood_id: Optional[int] = Field(
        default=None, foreign_key="neighborhoods.id", nullable=True
    )
    street: Optional[str] = Field(default=None, nullable=True)
    house_number: Optional[str] = Field(default=None, nullable=True)
    address_complement: Optional[str] = Field(default=None, nullable=True)
    cep: Optional[str] = Field(default=None, nullable=True)

    # Documents
    cpf: Optional[str] = Field(default=None, nullable=True)
    rg: Optional[str] = Field(default=None, nullable=True)
    issuing_body: Optional[str] = Field(default=None, nullable=True)
    date_issue: Optional[str] = Field(default=None, nullable=True)
    education_level: Optional[str] = Field(default=None, nullable=True)
    military_cert: Optional[str] = Field(default=None, nullable=True)
    pis_number: Optional[str] = Field(default=None, nullable=True)
    pis_date_register: Optional[str] = Field(default=None, nullable=True)
    electoral_title: Optional[str] = Field(default=None, nullable=True)
    electoral_zone: Optional[str] = Field(default=None, nullable=True)
    electoral_section: Optional[str] = Field(default=None, nullable=True)
    ctps: Optional[str] = Field(default=None, nullable=True)
    ctps_series: Optional[str] = Field(default=None, nullable=True)
    ctps_uf: Optional[str] = Field(default=None, nullable=True)
    ctps_issue_date: Optional[str] = Field(default=None, nullable=True)
    cnh: Optional[str] = Field(default=None, nullable=True)
    cnh_category: Optional[str] = Field(default=None, nullable=True)
    cnh_issue_date: Optional[str] = Field(default=None, nullable=True)
    cnh_expiration: Optional[str] = Field(default=None, nullable=True)

    # Employment Information
    first_job: Optional[bool] = Field(default=None, nullable=True)
    former_employee: Optional[bool] = Field(default=None, nullable=True)
    union_contribution: Optional[bool] = Field(default=None, nullable=True)
    unemployment_insurance: Optional[bool] = Field(default=None, nullable=True)
    previous_experience: Optional[bool] = Field(default=None, nullable=True)

    # Salary Information
    monthly_salary: Optional[float] = Field(default=None, nullable=True)
    hourly_salary: Optional[float] = Field(default=None, nullable=True)
    proportional_salary: Optional[float] = Field(default=None, nullable=True)
    hazardous_exposure: Optional[bool] = Field(default=None, nullable=True)

    # Timestamps
    # created_at: Optional[str] = Field(default=None, nullable=True)
    # updated_at: Optional[str] = Field(default=None, nullable=True)
