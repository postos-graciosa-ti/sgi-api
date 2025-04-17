from typing import Optional

from sqlmodel import Field, SQLModel


class Workers(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    enrolment: str = Field(default=None, nullable=True)
    name: str = Field(index=True)
    subsidiarie_id: int = Field(default=None, foreign_key="subsidiarie.id")
    is_active: bool = Field(default=True)
    is_away: bool = Field(default=False)
    away_reason_id: int = Field(
        default=None, nullable=True, foreign_key="awayreasons.id"
    )
    away_start_date: str = Field(default=None, nullable=True)
    away_end_date: str = Field(default=None, nullable=True)
    time_away: str = Field(default=None, nullable=True)
    esocial: str = Field(default=None, nullable=True)
    function_id: int = Field(default=None, foreign_key="function.id")
    cbo: str = Field(default=None, nullable=True)
    general_function_code: str = Field(default=None, nullable=True)
    cost_center_id: int = Field(default=None, foreign_key="costcenter.id")
    hierarchy_structure: int = Field(
        default=None, nullable=True, foreign_key="hierarchystructure.id"
    )
    department_id: int = Field(default=None, foreign_key="department.id")
    gender_id: int = Field(default=None, nullable=True, foreign_key="genders.id")
    ctps: str = Field(default=None, nullable=True)
    ctps_serie: str = Field(default=None, nullable=True)
    ctps_state: int = Field(default=None, nullable=True, foreign_key="states.id")
    ctps_emission_date: str = Field(default=None, nullable=True)
    pis: str = Field(default=None, nullable=True)
    pis_register_date: str = Field(default=None, nullable=True)
    cpf: str = Field(default=None, nullable=True)
    rg: str = Field(default=None, nullable=True)
    rg_issuing_agency: str = Field(default=None, nullable=True)
    rg_state: int = Field(default=None, nullable=True, foreign_key="states.id")
    rg_expedition_date: str = Field(default=None, nullable=True)
    fathername: str = Field(default=None, nullable=True)
    mothername: str = Field(default=None, nullable=True)
    birthdate: str = Field(default=None, nullable=True)
    birthcity: int = Field(default=None, nullable=True, foreign_key="cities.id")
    birthstate: int = Field(default=None, nullable=True, foreign_key="states.id")
    nationality: str = Field(default=None, nullable=True)
    admission_date: str = Field(default=None, nullable=True)
    enterprise_time: str = Field(default=None, nullable=True)
    wage: str = Field(default=None, nullable=True)
    turn_id: int = Field(default=None, foreign_key="turn.id")
    first_review_date: str = Field(default=None, nullable=True)
    second_review_date: str = Field(default=None, nullable=True)
    ethnicity_id: int = Field(default=None, nullable=True, foreign_key="ethnicity.id")
    civil_status_id: int = Field(
        default=None, nullable=True, foreign_key="civilstatus.id"
    )
    last_function_date: str = Field(default=None, nullable=True)
    current_function_time: str = Field(default=None, nullable=True)
    email: str = Field(default=None, nullable=True)
    school_level: int = Field(
        default=None, nullable=True, foreign_key="schoollevels.id"
    )
    street: str = Field(default=None, nullable=True)
    street_number: str = Field(default=None, nullable=True)
    street_complement: str = Field(default=None, nullable=True)
    neighborhood_id: int = Field(
        default=None, nullable=True, foreign_key="neighborhoods.id"
    )
    cep: str = Field(default=None, nullable=True)
    city: int = Field(default=None, nullable=True, foreign_key="cities.id")
    state: int = Field(default=None, nullable=True, foreign_key="states.id")
    phone: str = Field(default=None, nullable=True)
    mobile: str = Field(default=None, nullable=True)
    emergency_number: str = Field(default=None, nullable=True)
    bank: int = Field(default=None, nullable=True, foreign_key="banks.id")
    bank_agency: str = Field(default=None, nullable=True)
    bank_account: str = Field(default=None, nullable=True)

    resignation_date: str = Field(index=True)
    resignation_reason_id: Optional[int] = Field(
        default=None, foreign_key="resignablereasons.id", nullable=True
    )
    sales_code: str = Field(default=None, nullable=True)
    picture: str = Field(default=None, nullable=True)
    timecode: str = Field(default=None, nullable=True)
    has_children: bool | None = Field(default=None, nullable=True)
    children_data: str = Field(default="[]")
    military_cert_number: str = Field(default=None, nullable=True)
    votant_title: str = Field(default=None, nullable=True)
    votant_zone: str = Field(default=None, nullable=True)
    votant_session: str = Field(default=None, nullable=True)
    cnh: str = Field(default=None, nullable=True)
    # cnh_category: str = Field(default=None, nullable=True)
    cnh_category: int = Field(
        default=None, foreign_key="cnhcategories.id", nullable=True
    )
    cnh_emition_date: str = Field(default=None, nullable=True)
    cnh_valid_date: str = Field(default=None, nullable=True)
    first_job: bool | None = Field(default=None, nullable=True)
    was_employee: bool | None = Field(default=None, nullable=True)
    union_contribute_current_year: bool | None = Field(default=None, nullable=True)
    receiving_unemployment_insurance: bool | None = Field(default=None, nullable=True)
    previous_experience: bool | None = Field(default=None, nullable=True)
    month_wage: str = Field(default=None, nullable=True)
    hour_wage: str = Field(default=None, nullable=True)
    journey_wage: str = Field(default=None, nullable=True)
    transport_voucher: str = Field(default=None, nullable=True)
    transport_voucher_quantity: str = Field(default=None, nullable=True)
    diary_workjourney: str = Field(default=None, nullable=True)
    week_workjourney: str = Field(default=None, nullable=True)
    month_workjourney: str = Field(default=None, nullable=True)
    experience_time: str = Field(default=None, nullable=True)
    nocturne_hours: str = Field(default=None, nullable=True)
    dangerousness: bool | None = Field(default=None, nullable=True)
    unhealthy: bool | None = Field(default=None, nullable=True)
    wage_payment_method: int = Field(
        default=None, foreign_key="wagepaymentmethod.id", nullable=True
    )
    early_payment: bool | None = Field(default=None, nullable=True)
    harmfull_exposition: bool | None = Field(default=None, nullable=True)
