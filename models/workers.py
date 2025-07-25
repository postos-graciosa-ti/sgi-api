from typing import List, Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Workers(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    subsidiarie_id: int = Field(default=None, foreign_key="subsidiarie.id", index=True)
    away_reason_id: int = Field(
        default=None, nullable=True, foreign_key="awayreasons.id", index=True
    )
    function_id: int = Field(default=None, foreign_key="function.id", index=True)
    cost_center_id: int = Field(default=None, foreign_key="costcenter.id", index=True)
    hierarchy_structure: int = Field(
        default=None, nullable=True, foreign_key="hierarchystructure.id", index=True
    )
    department_id: int = Field(default=None, foreign_key="department.id", index=True)
    gender_id: int = Field(
        default=None, nullable=True, foreign_key="genders.id", index=True
    )
    ctps_state: int = Field(
        default=None, nullable=True, foreign_key="states.id", index=True
    )
    rg_state: int = Field(
        default=None, nullable=True, foreign_key="states.id", index=True
    )
    birthcity: int = Field(
        default=None, nullable=True, foreign_key="cities.id", index=True
    )
    birthstate: int = Field(
        default=None, nullable=True, foreign_key="states.id", index=True
    )
    turn_id: int = Field(default=None, foreign_key="turn.id", index=True)
    ethnicity_id: int = Field(
        default=None, nullable=True, foreign_key="ethnicity.id", index=True
    )
    civil_status_id: int = Field(
        default=None, nullable=True, foreign_key="civilstatus.id", index=True
    )
    school_level: int = Field(
        default=None, nullable=True, foreign_key="schoollevels.id", index=True
    )
    neighborhood_id: int = Field(
        default=None, nullable=True, foreign_key="neighborhoods.id", index=True
    )
    city: int = Field(default=None, nullable=True, foreign_key="cities.id", index=True)
    state: int = Field(default=None, nullable=True, foreign_key="states.id", index=True)
    bank: int = Field(default=None, nullable=True, foreign_key="banks.id", index=True)
    resignation_reason_id: Optional[int] = Field(
        default=None, foreign_key="resignablereasons.id", nullable=True, index=True
    )
    cnh_category: int = Field(
        default=None, foreign_key="cnhcategories.id", nullable=True, index=True
    )
    wage_payment_method: int = Field(
        default=None, foreign_key="wagepaymentmethod.id", nullable=True, index=True
    )

    enrolment: str = Field(default=None, nullable=True)
    name: str = Field(index=True)
    is_active: bool = Field(default=True)
    is_away: bool = Field(default=False)
    away_start_date: str = Field(default=None, nullable=True)
    away_end_date: str = Field(default=None, nullable=True)
    time_away: str = Field(default=None, nullable=True)
    esocial: str = Field(default=None, nullable=True)
    cbo: str = Field(default=None, nullable=True)
    general_function_code: str = Field(default=None, nullable=True)
    ctps: str = Field(default=None, nullable=True)
    ctps_serie: str = Field(default=None, nullable=True)
    ctps_emission_date: str = Field(default=None, nullable=True)
    pis: str = Field(default=None, nullable=True)
    pis_register_date: str = Field(default=None, nullable=True)
    cpf: str = Field(default=None, nullable=True)
    rg: str = Field(default=None, nullable=True)
    rg_issuing_agency: str = Field(default=None, nullable=True)
    rg_expedition_date: str = Field(default=None, nullable=True)
    fathername: str = Field(default=None, nullable=True)
    mothername: str = Field(default=None, nullable=True)
    birthdate: str = Field(default=None, nullable=True)
    nationality: str = Field(default=None, nullable=True)
    admission_date: str = Field(default=None, nullable=True)
    enterprise_time: str = Field(default=None, nullable=True)
    wage: str = Field(default=None, nullable=True)
    first_review_date: str = Field(default=None, nullable=True)
    second_review_date: str = Field(default=None, nullable=True)
    last_function_date: str = Field(default=None, nullable=True)
    current_function_time: str = Field(default=None, nullable=True)
    email: str = Field(default=None, nullable=True)
    street: str = Field(default=None, nullable=True)
    street_number: str = Field(default=None, nullable=True)
    street_complement: str = Field(default=None, nullable=True)
    cep: str = Field(default=None, nullable=True)
    phone: str = Field(default=None, nullable=True)
    mobile: str = Field(default=None, nullable=True)
    emergency_number: str = Field(default=None, nullable=True)
    bank_agency: str = Field(default=None, nullable=True)
    bank_account: str = Field(default=None, nullable=True)
    resignation_date: str = Field(index=True)
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
    early_payment: bool | None = Field(default=None, nullable=True)
    harmfull_exposition: bool | None = Field(default=None, nullable=True)
    has_experience_time: bool | None = Field(default=None, nullable=True)
    has_nocturne_hours: bool | None = Field(default=None, nullable=True)
    propotional_payment: bool | None = Field(default=None, nullable=True)
    total_nocturne_workjourney: str = Field(default=None, nullable=True)
    twenty_five_workjourney: str = Field(default=None, nullable=True)
    twenty_two_to_five_week_workjourney: str = Field(default=None, nullable=True)
    twenty_two_to_five_month_workjourney: str = Field(default=None, nullable=True)
    twenty_two_to_five_effective_diary_workjourney: str = Field(
        default=None, nullable=True
    )
    healthcare_plan: bool | None = Field(default=None, nullable=True)
    healthcare_plan_discount: str = Field(default=None, nullable=True)
    life_insurance: bool | None = Field(default=None, nullable=True)
    life_insurance_discount: str = Field(default=None, nullable=True)
    ag: str = Field(default=None, nullable=True)
    cc: str = Field(default=None, nullable=True)
    early_payment_discount: str = Field(default=None, nullable=True)

    app_login: str = Field(default=None, nullable=True)
    app_password: str = Field(default=None, nullable=True)


class WorkerDeactivateInput(BaseModel):
    is_active: bool
    resignation_date: str
    resignation_reason: int


class PatchWorkersTurnBody(BaseModel):
    worker_id: int
    turn_id: int
    function_id: int


class GetWorkersVtReportBody(BaseModel):
    start_date: str
    end_date: str


class RequestBadgesBody(BaseModel):
    workers_ids: List[int]
    recipient_email: str


class WorkersAway(BaseModel):
    away_start_date: str
    away_end_date: str
    away_reason_id: int


class MetricsUpdateRequest(BaseModel):
    metrics: str
