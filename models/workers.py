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

    # gender_id: int = Field(default=None, nullable=True, foreign_key="genders.id")
    # civil_status_id: int = Field(
    #     default=None, nullable=True, foreign_key="civilstatus.id"
    # )

    # street: str = Field(default=None, nullable=True)
    # street_number: str = Field(default=None, nullable=True)
    # street_complement: str = Field(default=None, nullable=True)
    # neighborhood_id: int = Field(
    #     default=None, nullable=True, foreign_key="neighborhoods.id"
    # )
    # cep: str = Field(default=None, nullable=True)
    # city: int = Field(default=None, nullable=True, foreign_key="cities.id")
    # state: int = Field(default=None, nullable=True, foreign_key="states.id")

    # phone: str = Field(default=None, nullable=True)
    # mobile: str = Field(default=None, nullable=True)
    # email: str = Field(default=None, nullable=True)
    # ethnicity_id: int = Field(default=None, nullable=True, foreign_key="ethnicity.id")

    # birthdate: str = Field(default=None, nullable=True)
    # birthcity: int = Field(default=None, nullable=True, foreign_key="cities.id")
    # birthstate: int = Field(default=None, nullable=True, foreign_key="states.id")
    # nationality: str = Field(default=None, nullable=True)

    # fathername: str = Field(default=None, nullable=True)
    # mothername: str = Field(default=None, nullable=True)

    # has_children: bool | None = Field(default=None, nullable=True)
    # children_data: str = Field(default="[]")

    # school_level

    # cpf: str = Field(default=None, nullable=True)
    # rg: str = Field(default=None, nullable=True)
    # rg_issuing_agency: str = Field(default=None, nullable=True)
    # rg_state: int = Field(default=None, nullable=True, foreign_key="states.id")
    # rg_expedition_date: str = Field(default=None, nullable=True)

    # military_cert_number: str = Field(default=None, nullable=True)
    # pis: str = Field(default=None, nullable=True)
    # pis_register_date: str = Field(default=None, nullable=True)

    # votant_title: str = Field(default=None, nullable=True)
    # votant_zone: str = Field(default=None, nullable=True)
    # votant_session: str = Field(default=None, nullable=True)

    # ctps: str = Field(default=None, nullable=True)
    # ctps_serie: str = Field(default=None, nullable=True)
    # ctps_state: int = Field(default=None, nullable=True, foreign_key="states.id")
    # ctps_emission_date: str = Field(default=None, nullable=True)

    # cnh: str = Field(default=None, nullable=True)
    # cnh_category: str = Field(default=None, nullable=True)
    # cnh_emition_date: str = Field(default=None, nullable=True)
    # cnh_valid_date: str = Field(default=None, nullable=True)

    # first_job: bool | None = Field(default=None, nullable=True)
    # was_employee: bool | None = Field(default=None, nullable=True)
    # union_contribute_current_year: bool | None = Field(default=None, nullable=True)
    # receiving_unemployment_insurance: bool | None = Field(default=None, nullable=True)
    # previous_experience: bool | None = Field(default=None, nullable=True)

    # month_wage: str = Field(default=None, nullable=True)
    # hour_wage: str = Field(default=None, nullable=True)
    # journey_wage: str = Field(default=None, nullable=True)

    # transport_voucher: str = Field(default=None, nullable=True)
    # transport_voucher_quantity: str = Field(default=None, nullable=True)
    
    # diary_workjourney: str = Field(default=None, nullable=True)
    # week_workjourney: str = Field(default=None, nullable=True)
    # month_workjourney: str = Field(default=None, nullable=True)

    # experience_time: str = Field(default=None, nullable=True)
    # nocturne_hours: str = Field(default=None, nullable=True)

    # dangerousness: bool | None = Field(default=None, nullable=True)
    # unhealthy: bool | None = Field(default=None, nullable=True)
    # wage_payment_method: str = Field(default=None, nullable=True)