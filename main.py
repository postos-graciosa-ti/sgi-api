import threading
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from sqlmodel import Session, select

from controllers.all_subsidiaries_no_review import (
    handle_get_workers_without_first_review_in_range_all,
    handle_get_workers_without_second_review_in_range_all,
)
from controllers.applicants import handle_get_applicants, handle_post_applicant
from controllers.banks import handle_get_banks
from controllers.candidates import (
    handle_get_candidates,
    handle_get_candidates_by_status,
    handle_post_candidate,
)
from controllers.cnh_categories import handle_get_cnh_categories
from controllers.cost_center import (
    handle_delete_cost_center,
    handle_get_cost_center,
    handle_get_cost_center_by_id,
    handle_post_cost_center,
    handle_put_cost_center,
)
from controllers.cost_center_log import (
    handle_get_cost_center_logs,
    handle_post_cost_center_logs,
)
from controllers.departments import (
    handle_delete_department,
    handle_get_department_by_id,
    handle_get_departments,
    handle_post_department,
    handle_put_department,
)
from controllers.departments_logs import (
    handle_get_departments_logs,
    handle_post_departments_logs,
)
from controllers.functions import (
    handle_delete_function,
    handle_get_functions,
    handle_get_functions_by_subsidiarie,
    handle_get_functions_for_users,
    handle_get_functions_for_workers,
    handle_post_function,
    handle_put_function,
)
from controllers.functions_logs import (
    handle_get_functions_logs,
    handle_post_functions_logs,
)
from controllers.hierarchy_structure import handle_get_hierarchy_structure
from controllers.hollidays_scale import (
    handle_delete_hollidays_scale,
    handle_get_hollidays_scale,
    handle_post_hollidays_scale,
)
from controllers.jobs import (
    handle_delete_job,
    handle_get_jobs,
    handle_get_jobs_by_subsidiarie_id,
    handle_post_job,
)
from controllers.months import handle_get_months
from controllers.nationalities import (
    handle_delete_nationalities,
    handle_get_nationalities,
    handle_post_nationalities,
    handle_put_nationalities,
)
from controllers.parents_type import handle_get_parents_type
from controllers.resignable_reasons import (
    handle_get_resignable_reasons,
    handle_resignable_reasons_report,
)
from controllers.roles import handle_get_roles
from controllers.root import (
    handle_get_docs_info,
    handle_health_check,
    handle_on_startup,
)
from controllers.scale import (
    handle_delete_scale,
    handle_get_days_off_quantity,
    handle_get_scales_by_subsidiarie_and_worker_id,
    handle_get_scales_by_subsidiarie_id,
    handle_handle_scale,
    handle_post_scale,
    handle_post_some_workers_scale,
    handle_post_subsidiarie_scale_to_print,
)
from controllers.scales_reports import (
    handle_generate_scale_days_off_report,
    handle_generate_scale_days_on_report,
)
from controllers.school_levels import handle_get_school_levels
from controllers.states import (
    handle_delete_states,
    handle_get_states,
    handle_get_states_by_id,
    handle_get_states_by_nationalitie,
    handle_post_states,
    handle_put_states,
)
from controllers.subsidiaries import (
    handle_delete_subsidiarie,
    handle_get_subsidiarie_by_id,
    handle_get_subsidiaries,
    handle_post_subsidiaries,
)
from controllers.subsidiaries_logs import (
    handle_get_subsidiarie_logs,
    handle_post_subsidiaries_logs,
)
from controllers.subsidiaries_notifications import (
    handle_get_subsidiarie_notifications,
    handle_get_subsidiaries_status,
)
from controllers.turn import (
    handle_delete_turn,
    handle_get_subsidiarie_turns,
    handle_get_turn_by_id,
    handle_get_turns,
    handle_post_turns,
    handle_put_turn,
)
from controllers.turns_logs import handle_get_turns_logs, handle_post_turns_logs
from controllers.users import (
    handle_change_password,
    handle_confirm_password,
    handle_create_user_password,
    handle_delete_user,
    handle_get_test,
    handle_get_user_by_id,
    handle_get_users,
    handle_get_users_roles,
    handle_post_user,
    handle_put_user,
    handle_user_login,
)
from controllers.users_logs import handle_get_logs_user, handle_post_logs_user
from controllers.wage_payment_method import handle_get_wage_payment_method
from controllers.workers import (
    handle_deactivate_worker,
    handle_delete_worker_notation,
    handle_get_active_workers_by_subsidiarie_and_function,
    handle_get_active_workers_by_turn_and_subsidiarie,
    handle_get_worker_by_id,
    handle_get_worker_notations,
    handle_get_workers_by_subsidiarie,
    handle_get_workers_by_subsidiaries_functions_and_turns,
    handle_get_workers_by_turn_and_subsidiarie,
    handle_post_worker,
    handle_post_worker_notation,
    handle_put_worker,
    handle_reactivate_worker,
)
from controllers.workers_logs import (
    handle_get_create_workers_logs,
    handle_get_delete_workers_logs,
    handle_get_update_workers_logs,
    handle_post_create_workers_logs,
    handle_post_delete_workers_logs,
    handle_post_update_workers_logs,
    handle_post_workers_logs,
)
from controllers.workers_parents import (
    handle_delete_workers_parents,
    handle_get_workers_parents,
    handle_post_workers_parents,
)
from database.sqlite import engine
from functions.auth import verify_token
from functions.error_handling import error_handler
from keep_alive import keep_alive_function
from middlewares.cors_middleware import add_cors_middleware
from models.applicants import Applicants
from models.away_reasons import AwayReasons
from models.banks import Banks
from models.candidate import Candidate
from models.cities import Cities
from models.civil_status import CivilStatus
from models.cnh_categories import CnhCategories
from models.cost_center import CostCenter
from models.cost_center_logs import CostCenterLogs
from models.dates_events import DatesEvents
from models.department import Department
from models.department_logs import DepartmentsLogs
from models.ethnicity import Ethnicity
from models.function import Function
from models.function_logs import FunctionLogs
from models.genders import Genders
from models.hollidays_scale import HollidaysScale
from models.jobs import Jobs
from models.nationalities import Nationalities
from models.neighborhoods import Neighborhoods
from models.parents_type import ParentsType
from models.role import Role
from models.scale_logs import ScaleLogs
from models.school_levels import SchoolLevels
from models.states import States
from models.subsidiarie import Subsidiarie
from models.subsidiarie_logs import SubsidiarieLogs
from models.turn import Turn
from models.TurnsLogs import TurnsLogs
from models.user import User
from models.users_logs import UsersLogs
from models.wage_payment_method import WagePaymentMethod
from models.workers import Workers
from models.workers_first_review import WorkersFirstReview
from models.workers_logs import WorkersLogs
from models.workers_parents import WorkersParents
from models.workers_second_review import WorkersSecondReview
from pyhints.no_reviews import SubsidiaryFilter
from pyhints.resignable_reasons import StatusResignableReasonsInput
from pyhints.scales import (
    PostScaleInput,
    PostSomeWorkersScaleInput,
    ScalesPrintInput,
    ScalesReportInput,
    WorkerDeactivateInput,
)
from pyhints.turns import PutTurn
from pyhints.users import (
    ChangeUserPasswordInput,
    ConfirmPassword,
    CreateUserPasswordInput,
    Test,
)
from pyhints.workers import (
    PostWorkerNotationInput,
    WorkerLogCreateInput,
    WorkerLogDeleteInput,
    WorkerLogUpdateInput,
)
from scripts.excel_scraping import handle_excel_scraping

# pre settings

load_dotenv()

app = FastAPI()

add_cors_middleware(app)

threading.Thread(target=keep_alive_function, daemon=True).start()

# startup function


@app.on_event("startup")
def on_startup():
    return handle_on_startup()


# public routes


@app.get("/")
def get_docs_info():
    return handle_get_docs_info()


@app.get("/health-check")
def health_check():
    return handle_health_check()


@app.post("/users/login")
def user_login(user: User):
    return handle_user_login(user)


@app.post("/users/create-password")
def create_user_password(userData: CreateUserPasswordInput):
    return handle_create_user_password(userData)


@app.post("/subsidiaries/{id}/scripts/excel-scraping")
async def excel_scraping(id: int, file: UploadFile = File(...)):
    return await handle_excel_scraping(id, file)


# users


@app.get("/users", dependencies=[Depends(verify_token)])
@error_handler
def get_users():
    return handle_get_users()


@app.get("/users/{id}", dependencies=[Depends(verify_token)])
@error_handler
def get_user_by_id(id: int):
    return handle_get_user_by_id(id)


@app.get("/users_roles", dependencies=[Depends(verify_token)])
@error_handler
def get_users_roles():
    return handle_get_users_roles()


@app.post("/users", dependencies=[Depends(verify_token)])
@error_handler
def post_user(user: User):
    return handle_post_user(user)


@app.put("/users/{id}", dependencies=[Depends(verify_token)])
@error_handler
def put_user(id: int, user: User):
    return handle_put_user(id, user)


@app.delete("/users/{id}", dependencies=[Depends(verify_token)])
@error_handler
def delete_user(id: int):
    return handle_delete_user(id)


@app.post("/test", dependencies=[Depends(verify_token)])
@error_handler
def test(arr: Test):
    return handle_get_test(arr)


@app.post("/confirm-password", dependencies=[Depends(verify_token)])
@error_handler
def confirm_password(userData: ConfirmPassword):
    return handle_confirm_password(userData)


@app.post("/users/change-password", dependencies=[Depends(verify_token)])
@error_handler
def change_password(userData: ChangeUserPasswordInput):
    return handle_change_password(userData)


# user logs


@app.get("/logs/users", dependencies=[Depends(verify_token)])
@error_handler
def get_logs_user():
    return handle_get_logs_user()


@app.post("/logs/users", dependencies=[Depends(verify_token)])
@error_handler
def post_logs_user(users_logs: UsersLogs):
    return handle_post_logs_user(users_logs)


# months


@app.get("/months", dependencies=[Depends(verify_token)])
@error_handler
def get_months():
    return handle_get_months()


# subsidiaries


@app.get("/subsidiaries", dependencies=[Depends(verify_token)])
@error_handler
def get_subsidiaries():
    return handle_get_subsidiaries()


@app.get("/subsidiaries/{id}", dependencies=[Depends(verify_token)])
@error_handler
def get_subsidiarie_by_id(id: int):
    return handle_get_subsidiarie_by_id(id)


@app.post("/subsidiaries", dependencies=[Depends(verify_token)])
@error_handler
def post_subsidiaries(formData: Subsidiarie):
    return handle_post_subsidiaries(formData)


@app.put("/subsidiaries/{id}", dependencies=[Depends(verify_token)])
@error_handler
def put_subsidiarie(id: int, subsidiarie: Subsidiarie):
    with Session(engine) as session:
        db_subsidiarie = session.exec(
            select(Subsidiarie).where(Subsidiarie.id == id)
        ).first()

        if subsidiarie.name and subsidiarie.name != db_subsidiarie.name:
            db_subsidiarie.name = subsidiarie.name

        if subsidiarie.adress and subsidiarie.adress != db_subsidiarie.adress:
            db_subsidiarie.adress = subsidiarie.adress

        if subsidiarie.phone and subsidiarie.phone != db_subsidiarie.phone:
            db_subsidiarie.phone = subsidiarie.phone

        if subsidiarie.email and subsidiarie.email != db_subsidiarie.email:
            db_subsidiarie.email = subsidiarie.email

        if (
            subsidiarie.coordinator is not None
            and subsidiarie.coordinator != db_subsidiarie.coordinator
        ):
            db_subsidiarie.coordinator = subsidiarie.coordinator

        if (
            subsidiarie.manager is not None
            and subsidiarie.manager != db_subsidiarie.manager
        ):
            db_subsidiarie.manager = subsidiarie.manager

        session.add(db_subsidiarie)

        session.commit()

        session.refresh(db_subsidiarie)

        return db_subsidiarie


@app.delete("/subsidiaries/{id}", dependencies=[Depends(verify_token)])
@error_handler
def delete_subsidiaries(id: int):
    return handle_delete_subsidiarie(id)


# subsidiaries notifications


@app.get("/subsidiaries/{id}/notifications", dependencies=[Depends(verify_token)])
@error_handler
async def get_subsidiarie_notifications(id: int):
    return await handle_get_subsidiarie_notifications(id)


@app.get("/subsidiaries/{id}/workers-status", dependencies=[Depends(verify_token)])
@error_handler
def get_subsidiaries_status(id: int):
    handle_get_subsidiaries_status(id)


# subsidiaries logs


@app.get("/subsidiaries-logs", dependencies=[Depends(verify_token)])
@error_handler
def get_subsidiarie_logs():
    return handle_get_subsidiarie_logs()


@app.post("/subsidiaries/logs", dependencies=[Depends(verify_token)])
@error_handler
def post_subsidiaries_logs(subsidiarie_log: SubsidiarieLogs):
    return handle_post_subsidiaries_logs(subsidiarie_log)


# turns


@app.get("/subsidiaries/{id}/turns", dependencies=[Depends(verify_token)])
@error_handler
def get_subsidiarie_turns(id: int):
    return handle_get_subsidiarie_turns(id)


@app.get("/turns", dependencies=[Depends(verify_token)])
@error_handler
def get_turns():
    return handle_get_turns()


@app.get("/turns/{id}", dependencies=[Depends(verify_token)])
@error_handler
def get_turn_by_id(id: int):
    return handle_get_turn_by_id(id)


@app.post("/turns", dependencies=[Depends(verify_token)])
@error_handler
def post_turns(formData: Turn):
    return handle_post_turns(formData)


@app.put("/turns/{id}", dependencies=[Depends(verify_token)])
@error_handler
def put_turn(id: int, formData: PutTurn):
    return handle_put_turn(id, formData)


@app.delete("/turns/{id}", dependencies=[Depends(verify_token)])
@error_handler
def delete_turn(id: int):
    return handle_delete_turn(id)


# turns logs


@app.get("/subsidiaries/{id}/logs/turns", dependencies=[Depends(verify_token)])
@error_handler
def get_turns_logs(id: int):
    return handle_get_turns_logs(id)


@app.post("/subsidiaries/{id}/logs/turns", dependencies=[Depends(verify_token)])
@error_handler
def post_turns_logs(id: int, turn_log: TurnsLogs):
    return handle_post_turns_logs(id, turn_log)


# workers


@app.get("/workers/{id}", dependencies=[Depends(verify_token)])
@error_handler
def get_worker_by_id(id: int):
    return handle_get_worker_by_id(id)


@app.get(
    "/workers/turns/{turn_id}/subsidiarie/{subsidiarie_id}",
    dependencies=[Depends(verify_token)],
)
@error_handler
def get_workers_by_turn_and_subsidiarie(turn_id: int, subsidiarie_id: int):
    return handle_get_workers_by_turn_and_subsidiarie(turn_id, subsidiarie_id)


@app.get(
    "/workers/on-track/turn/{turn_id}/subsidiarie/{subsidiarie_id}",
    dependencies=[Depends(verify_token)],
)
@error_handler
def get_active_workers_by_turn_and_subsidiarie(turn_id: int, subsidiarie_id: int):
    return handle_get_active_workers_by_turn_and_subsidiarie(turn_id, subsidiarie_id)


@app.get(
    "/workers/active/subsidiarie/{subsidiarie_id}/function/{function_id}",
    dependencies=[Depends(verify_token)],
)
@error_handler
def get_active_workers_by_subsidiarie_and_function(
    subsidiarie_id: int, function_id: int
):
    return handle_get_active_workers_by_subsidiarie_and_function(
        subsidiarie_id, function_id
    )


from sqlalchemy.orm import aliased

from models.hierarchy_structure import HierarchyStructure
from models.resignable_reasons import ResignableReasons


@app.get("/workers/subsidiarie/{subsidiarie_id}")
def handle_get_workers_by_subsidiarie(subsidiarie_id: int):
    # Criar aliases para tabelas que são referenciadas múltiplas vezes
    City = aliased(Cities)
    BirthCity = aliased(Cities)
    State = aliased(States)
    BirthState = aliased(States)
    RgState = aliased(States)
    CtpsState = aliased(States)

    with Session(engine) as session:
        # Consulta principal com todos os joins necessários
        query = (
            select(
                Workers,
                Function.name.label("function_name"),
                Turn.name.label("turn_name"),
                Turn.start_time.label("turn_start_time"),
                Turn.end_time.label("turn_end_time"),
                CostCenter.name.label("cost_center_name"),
                Department.name.label("department_name"),
                ResignableReasons.name.label("resignation_reason_name"),
                Genders.name.label("gender_name"),
                CivilStatus.name.label("civil_status_name"),
                Neighborhoods.name.label("neighborhood_name"),
                City.name.label("city_name"),
                State.name.label("state_name"),
                Ethnicity.name.label("ethnicity_name"),
                BirthCity.name.label("birthcity_name"),
                BirthState.name.label("birthstate_name"),
                RgState.name.label("rg_state_name"),
                CtpsState.name.label("ctps_state_name"),
                CnhCategories.name.label("cnh_category_name"),
                WagePaymentMethod.name.label("wage_payment_method_name"),
                AwayReasons.name.label("away_reason_name"),
                SchoolLevels.name.label("school_level_name"),
                Banks.name.label("bank_name"),
                Nationalities.name.label("nationality_name"),
                HierarchyStructure.name.label("hierarchy_structure_name"),
            )
            .where(Workers.subsidiarie_id == subsidiarie_id)
            # Joins principais
            .join(Function, Function.id == Workers.function_id)
            .join(Turn, Turn.id == Workers.turn_id)
            .join(CostCenter, CostCenter.id == Workers.cost_center_id)
            .join(Department, Department.id == Workers.department_id)
            .join(
                ResignableReasons,
                ResignableReasons.id == Workers.resignation_reason_id,
                isouter=True,
            )
            # Joins para campos relacionados
            .join(Genders, Genders.id == Workers.gender_id, isouter=True)
            .join(CivilStatus, CivilStatus.id == Workers.civil_status_id, isouter=True)
            .join(
                Neighborhoods, Neighborhoods.id == Workers.neighborhood_id, isouter=True
            )
            .join(City, City.id == Workers.city, isouter=True)
            .join(State, State.id == Workers.state, isouter=True)
            .join(Ethnicity, Ethnicity.id == Workers.ethnicity_id, isouter=True)
            .join(BirthCity, BirthCity.id == Workers.birthcity, isouter=True)
            .join(BirthState, BirthState.id == Workers.birthstate, isouter=True)
            .join(RgState, RgState.id == Workers.rg_state, isouter=True)
            .join(CtpsState, CtpsState.id == Workers.ctps_state, isouter=True)
            .join(CnhCategories, CnhCategories.id == Workers.cnh_category, isouter=True)
            .join(
                WagePaymentMethod,
                WagePaymentMethod.id == Workers.wage_payment_method,
                isouter=True,
            )
            .join(AwayReasons, AwayReasons.id == Workers.away_reason_id, isouter=True)
            .join(SchoolLevels, SchoolLevels.id == Workers.school_level, isouter=True)
            .join(Banks, Banks.id == Workers.bank, isouter=True)
            .join(Nationalities, Nationalities.id == Workers.nationality, isouter=True)
            .join(
                HierarchyStructure,
                HierarchyStructure.id == Workers.hierarchy_structure,
                isouter=True,
            )
            .order_by(Workers.name)
        )

        workers_data = session.exec(query).all()

        # Construir o resultado completo
        result = []
        for row in workers_data:
            worker = row[0]  # O primeiro elemento é o objeto Workers
            worker_dict = {
                "worker_id": worker.id,
                "worker_name": worker.name,
                "worker_is_active": worker.is_active,
                "admission_date": worker.admission_date,
                "resignation_date": worker.resignation_date,
                "resignation_reason_id": worker.resignation_reason_id,
                "resignation_reason_name": row.resignation_reason_name,
                "worker_enrolment": worker.enrolment,
                "worker_sales_code": worker.sales_code,
                "picture": worker.picture,
                "timecode": worker.timecode,
                "first_review_date": worker.first_review_date,
                "second_review_date": worker.second_review_date,
                "esocial": worker.esocial,
                "function_id": worker.function_id,
                "function_name": row.function_name,
                "turn_id": worker.turn_id,
                "turn_name": row.turn_name,
                "turn_start_time": row.turn_start_time,
                "turn_end_time": row.turn_end_time,
                "cost_center_id": worker.cost_center_id,
                "cost_center": row.cost_center_name,
                "department_id": worker.department_id,
                "department": row.department_name,
                "gender": (
                    {"id": worker.gender_id, "name": row.gender_name}
                    if worker.gender_id
                    else None
                ),
                "civil_status": (
                    {"id": worker.civil_status_id, "name": row.civil_status_name}
                    if worker.civil_status_id
                    else None
                ),
                "street": worker.street,
                "street_number": worker.street_number,
                "street_complement": worker.street_complement,
                "neighborhood": (
                    {"id": worker.neighborhood_id, "name": row.neighborhood_name}
                    if worker.neighborhood_id
                    else None
                ),
                "cep": worker.cep,
                "city": (
                    {"id": worker.city, "name": row.city_name} if worker.city else None
                ),
                "state": (
                    {"id": worker.state, "name": row.state_name}
                    if worker.state
                    else None
                ),
                "phone": worker.phone,
                "mobile": worker.mobile,
                "email": worker.email,
                "ethnicity": (
                    {"id": worker.ethnicity_id, "name": row.ethnicity_name}
                    if worker.ethnicity_id
                    else None
                ),
                "birthdate": worker.birthdate,
                "birthcity": (
                    {"id": worker.birthcity, "name": row.birthcity_name}
                    if worker.birthcity
                    else None
                ),
                "birthstate": (
                    {"id": worker.birthstate, "name": row.birthstate_name}
                    if worker.birthstate
                    else None
                ),
                "fathername": worker.fathername,
                "mothername": worker.mothername,
                "cpf": worker.cpf,
                "rg": worker.rg,
                "rg_issuing_agency": worker.rg_issuing_agency,
                "rg_state": (
                    {"id": worker.rg_state, "name": row.rg_state_name}
                    if worker.rg_state
                    else None
                ),
                "rg_expedition_date": worker.rg_expedition_date,
                "military_cert_number": worker.military_cert_number,
                "pis": worker.pis,
                "pis_register_date": worker.pis_register_date,
                "votant_session": worker.votant_session,
                "votant_title": worker.votant_title,
                "votant_zone": worker.votant_zone,
                "ctps": worker.ctps,
                "ctps_serie": worker.ctps_serie,
                "ctps_state": (
                    {"id": worker.ctps_state, "name": row.ctps_state_name}
                    if worker.ctps_state
                    else None
                ),
                "ctps_emission_date": worker.ctps_emission_date,
                "cnh": worker.cnh,
                "cnh_category": (
                    {"id": worker.cnh_category, "name": row.cnh_category_name}
                    if worker.cnh_category
                    else None
                ),
                "cnh_emition_date": worker.cnh_emition_date,
                "cnh_valid_date": worker.cnh_valid_date,
                "first_job": worker.first_job,
                "was_employee": worker.was_employee,
                "union_contribute_current_year": worker.union_contribute_current_year,
                "receiving_unemployment_insurance": worker.receiving_unemployment_insurance,
                "previous_experience": worker.previous_experience,
                "month_wage": worker.month_wage,
                "hour_wage": worker.hour_wage,
                "journey_wage": worker.journey_wage,
                "transport_voucher": worker.transport_voucher,
                "transport_voucher_quantity": worker.transport_voucher_quantity,
                "diary_workjourney": worker.diary_workjourney,
                "week_workjourney": worker.week_workjourney,
                "month_workjourney": worker.month_workjourney,
                "experience_time": worker.experience_time,
                "nocturne_hours": worker.nocturne_hours,
                "dangerousness": worker.dangerousness,
                "unhealthy": worker.unhealthy,
                "wage_payment_method": (
                    {
                        "id": worker.wage_payment_method,
                        "name": row.wage_payment_method_name,
                    }
                    if worker.wage_payment_method
                    else None
                ),
                "is_away": worker.is_away,
                "away_reason": (
                    {"id": worker.away_reason_id, "name": row.away_reason_name}
                    if worker.away_reason_id
                    else None
                ),
                "away_start_date": worker.away_start_date,
                "away_end_date": worker.away_end_date,
                "general_function_code": worker.general_function_code,
                "wage": worker.wage,
                "last_function_date": worker.last_function_date,
                "current_function_time": worker.current_function_time,
                "school_level": (
                    {"id": worker.school_level, "name": row.school_level_name}
                    if worker.school_level
                    else None
                ),
                "emergency_number": worker.emergency_number,
                "bank": (
                    {"id": worker.bank, "name": row.bank_name} if worker.bank else None
                ),
                "bank_agency": worker.bank_agency,
                "bank_account": worker.bank_account,
                "nationality": (
                    {"id": worker.nationality, "name": row.nationality_name}
                    if worker.nationality
                    else None
                ),
                "has_children": worker.has_children,
                "hierarchy_structure": (
                    {
                        "id": worker.hierarchy_structure,
                        "name": row.hierarchy_structure_name,
                    }
                    if worker.hierarchy_structure
                    else None
                ),
                "enterprise_time": worker.enterprise_time,
                "cbo": worker.cbo,
                "early_payment": worker.early_payment,
                "harmfull_exposition": worker.harmfull_exposition,
                "has_experience_time": worker.has_experience_time,
            }
            result.append(worker_dict)

        return result


@app.get(
    "/workers/subsidiaries/{subsidiarie_id}/functions/{function_id}/turns/{turn_id}",
    dependencies=[Depends(verify_token)],
)
@error_handler
def get_workers_by_subsidiaries_functions_and_turns(
    subsidiarie_id: int, function_id: int, turn_id: int
):
    return handle_get_workers_by_subsidiaries_functions_and_turns(
        subsidiarie_id, function_id, turn_id
    )


@app.get(
    "/subsidiaries/{subsidiarie_id}/turns/{turn_id}/functions/{function_id}/workers",
    dependencies=[Depends(verify_token)],
)
@error_handler
def get_workers_by_turn_and_function(
    subsidiarie_id: int, turn_id: int, function_id: int
):
    with Session(engine) as session:
        workers = session.exec(
            select(Workers)
            .where(Workers.subsidiarie_id == subsidiarie_id)
            .where(Workers.turn_id == turn_id)
            .where(Workers.function_id == function_id)
        ).all()

        return workers


@app.get(
    "/subsidiaries/{subsidiarie_id}/turns/{turn_id}/workers",
    dependencies=[Depends(verify_token)],
)
@error_handler
def get_workers_by_turn(subsidiarie_id: int, turn_id: int):
    with Session(engine) as session:
        workers = session.exec(
            select(Workers)
            .where(Workers.subsidiarie_id == subsidiarie_id)
            .where(Workers.turn_id == turn_id)
        ).all()

        return workers


@app.post("/workers")
def post_worker(worker: Workers):
    admission_date = datetime.strptime(worker.admission_date, "%Y-%m-%d").date()

    first_review = admission_date + relativedelta(months=1)

    second_review = admission_date + relativedelta(months=2)

    worker.first_review_date = first_review.strftime("%Y-%m-%d")

    worker.second_review_date = second_review.strftime("%Y-%m-%d")

    with Session(engine) as session:
        session.add(worker)

        session.commit()

        session.refresh(worker)

        return worker


@app.put("/workers/{id}", dependencies=[Depends(verify_token)])
@error_handler
def put_worker(id: int, worker: Workers):
    return handle_put_worker(id, worker)


@app.put("/workers/{id}/deactivate", dependencies=[Depends(verify_token)])
@error_handler
def deactivate_worker(id: int, worker: WorkerDeactivateInput):
    return handle_deactivate_worker(id, worker)


@app.put("/workers/{id}/reactivate", dependencies=[Depends(verify_token)])
@error_handler
def reactivate_worker(id: int):
    return handle_reactivate_worker(id)


# workers logs


@app.get("/logs/subsidiaries/{id}/workers", dependencies=[Depends(verify_token)])
@error_handler
def get_workers_logs(id: int):
    with Session(engine) as session:
        query = select(WorkersLogs).where(WorkersLogs.subsidiarie_id == id)

        workers_logs = session.exec(query).all()

        return workers_logs


@app.post("/logs/subsidiaries/{id}/workers", dependencies=[Depends(verify_token)])
@error_handler
def post_workers_logs(id: int, workers_log: WorkersLogs):
    return handle_post_workers_logs(id, workers_log)


# workers logs create


@app.get("/logs/subsidiaries/{id}/workers/create", dependencies=[Depends(verify_token)])
@error_handler
def get_create_workers_logs(id: int):
    return handle_get_create_workers_logs(id)


@app.post(
    "/logs/subsidiaries/{id}/workers/create", dependencies=[Depends(verify_token)]
)
@error_handler
def post_create_workers_logs(id: int, worker_log: WorkerLogCreateInput):
    return handle_post_create_workers_logs(id, worker_log)


# workers logs update


@app.get("/logs/subsidiaries/{id}/workers/update", dependencies=[Depends(verify_token)])
@error_handler
def get_update_workers_logs(id: int):
    return handle_get_update_workers_logs(id)


@app.post(
    "/logs/subsidiaries/{id}/workers/update", dependencies=[Depends(verify_token)]
)
@error_handler
def post_update_workers_logs(id: int, worker_log: WorkerLogUpdateInput):
    return handle_post_update_workers_logs(id, worker_log)


# workers logs delete


@app.get("/logs/subsidiaries/{id}/workers/delete", dependencies=[Depends(verify_token)])
@error_handler
def get_delete_workers_logs(id: int):
    return handle_get_delete_workers_logs(id)


@app.post(
    "/logs/subsidiaries/{id}/workers/delete", dependencies=[Depends(verify_token)]
)
@error_handler
def post_delete_workers_logs(id: int, worker_log: WorkerLogDeleteInput):
    return handle_post_delete_workers_logs(id, worker_log)


# workers notations


@app.get("/workers/{id}/notations", dependencies=[Depends(verify_token)])
@error_handler
def get_worker_notations(id: int):
    return handle_get_worker_notations(id)


@app.post("/workers/{id}/notations", dependencies=[Depends(verify_token)])
@error_handler
def post_worker_notation(id: int, data: PostWorkerNotationInput):
    return handle_post_worker_notation(id, data)


@app.delete("/workers-notations/{id}", dependencies=[Depends(verify_token)])
@error_handler
def delete_worker_notation(id: int):
    return handle_delete_worker_notation(id)


# functions


@app.get("/subsidiaries/{id}/functions", dependencies=[Depends(verify_token)])
@error_handler
def get_functions_by_subsidiarie(id: int):
    return handle_get_functions_by_subsidiarie(id)


@app.get("/functions", dependencies=[Depends(verify_token)])
@error_handler
def get_functions():
    return handle_get_functions()


@app.get("/functions/for-users", dependencies=[Depends(verify_token)])
@error_handler
def get_functions_for_users():
    return handle_get_functions_for_users()


@app.get("/functions/for-workers", dependencies=[Depends(verify_token)])
@error_handler
def get_functions_for_users():
    return handle_get_functions_for_workers()


@app.post("/functions", dependencies=[Depends(verify_token)])
@error_handler
def post_function(function: Function):
    return handle_post_function(function)


@app.put("/functions/{id}", dependencies=[Depends(verify_token)])
@error_handler
def put_function(id: int, function: Function):
    return handle_put_function(id, function)


@app.delete("/functions/{id}", dependencies=[Depends(verify_token)])
@error_handler
def delete_function(id: int):
    return handle_delete_function(id)


# functions logs


@app.get("/subsidiaries/{id}/functions/logs", dependencies=[Depends(verify_token)])
@error_handler
def get_functions_logs(id: int):
    return handle_get_functions_logs(id)


@app.post("/subsidiaries/{id}/functions/logs", dependencies=[Depends(verify_token)])
@error_handler
def post_functions_logs(id: int, function_log: FunctionLogs):
    return handle_post_functions_logs(id, function_log)


# jobs


@app.get("/jobs", dependencies=[Depends(verify_token)])
@error_handler
def get_jobs():
    return handle_get_jobs()


@app.get("/jobs/subsidiarie/{subsidiarie_id}", dependencies=[Depends(verify_token)])
@error_handler
def get_jobs_by_subsidiarie_id(subsidiarie_id: int):
    return handle_get_jobs_by_subsidiarie_id(subsidiarie_id)


@app.post("/jobs", dependencies=[Depends(verify_token)])
@error_handler
def post_job(job: Jobs):
    return handle_post_job(job)


@app.delete("/jobs/{job_id}", dependencies=[Depends(verify_token)])
@error_handler
def delete_job(job_id: int):
    return handle_delete_job(job_id)


# roles


@app.get("/roles", dependencies=[Depends(verify_token)])
@error_handler
def get_roles():
    return handle_get_roles()


@app.get("/roles/{id}", dependencies=[Depends(verify_token)])
@error_handler
def get_roles_by_id(id: int):
    with Session(engine) as session:
        role = session.exec(select(Role).where(Role.id == id)).first()

        return role


# candidates


@app.get("/candidates", dependencies=[Depends(verify_token)])
@error_handler
def get_candidates():
    return handle_get_candidates()


@app.get("/candidates/status/{id}", dependencies=[Depends(verify_token)])
@error_handler
def get_candidates_by_status(id: int):
    return handle_get_candidates_by_status(id)


@app.post("/candidates", dependencies=[Depends(verify_token)])
@error_handler
def post_candidate(candidate: Candidate):
    return handle_post_candidate(candidate)


# scales


@app.get("/scales/subsidiaries/{subsidiarie_id}", dependencies=[Depends(verify_token)])
@error_handler
def get_scales_by_subsidiarie_id(subsidiarie_id: int):
    return handle_get_scales_by_subsidiarie_id(subsidiarie_id)


@app.get(
    "/scales/subsidiaries/{subsidiarie_id}/workers/{worker_id}",
    dependencies=[Depends(verify_token)],
)
@error_handler
def get_scales_by_subsidiarie_and_worker_id(subsidiarie_id: int, worker_id: int):
    return handle_get_scales_by_subsidiarie_and_worker_id(subsidiarie_id, worker_id)


@app.get("/scales/day-off/quantity", dependencies=[Depends(verify_token)])
@error_handler
def get_days_off_quantity():
    return handle_get_days_off_quantity()


@app.post("/scales", dependencies=[Depends(verify_token)])
@error_handler
def post_scale(form_data: PostScaleInput):
    return handle_post_scale(form_data)


@app.post("/scales/some-workers", dependencies=[Depends(verify_token)])
@error_handler
def post_some_workers_scale(form_data: PostSomeWorkersScaleInput):
    return handle_post_some_workers_scale(form_data)


@app.post("/delete-scale", dependencies=[Depends(verify_token)])
@error_handler
def handle_scale(form_data: PostScaleInput):
    return handle_handle_scale(form_data)


@app.delete(
    "/scales/{scale_id}/subsidiaries/{subsidiarie_id}",
    dependencies=[Depends(verify_token)],
)
@error_handler
def delete_scale(scale_id: int, subsidiarie_id: int):
    return handle_delete_scale(scale_id, subsidiarie_id)


# scale logs


@app.get("/subsidiaries/{id}/scales/logs", dependencies=[Depends(verify_token)])
@error_handler
def get_scales_logs(id: int):
    with Session(engine) as session:
        scales_logs = session.exec(
            select(ScaleLogs)
            .where(ScaleLogs.subsidiarie_id == id)
            .order_by(ScaleLogs.id.desc())
        ).all()

        return scales_logs


@app.post("/subsidiaries/{id}/scales/logs", dependencies=[Depends(verify_token)])
@error_handler
def post_scales_logs(id: int, scale_log: ScaleLogs):
    with Session(engine) as session:
        scale_log.subsidiarie_id = id

        session.add(scale_log)

        session.commit()

        session.refresh(scale_log)

        return scale_log


# scale reports


@app.post(
    "/reports/subsidiaries/{subsidiarie_id}/scales/days-on",
    dependencies=[Depends(verify_token)],
)
async def generate_scale_days_on_report(subsidiarie_id: int, input: ScalesReportInput):
    return await handle_generate_scale_days_on_report(subsidiarie_id, input)


@app.post(
    "/reports/subsidiaries/{subsidiarie_id}/scales/days-off",
    dependencies=[Depends(verify_token)],
)
async def generate_scale_days_off_report(subsidiarie_id: int, input: ScalesReportInput):
    return await handle_generate_scale_days_off_report(subsidiarie_id, input)


# scales print


@app.post("/subsidiaries/{id}/scales/print", dependencies=[Depends(verify_token)])
@error_handler
def post_subsidiarie_scale_to_print(id: int, scales_print_input: ScalesPrintInput):
    return handle_post_subsidiarie_scale_to_print(id, scales_print_input)


# cities


@app.get("/cities", dependencies=[Depends(verify_token)])
@error_handler
def get_cities():
    with Session(engine) as session:
        cities = session.exec(select(Cities)).all()

        return cities


@app.get("/states/{id}/cities")
def get_cities_by_state(id: int):
    with Session(engine) as session:
        cities = session.exec(select(Cities).where(Cities.state_id == id)).all()

        return cities


@app.get("/cities/{id}", dependencies=[Depends(verify_token)])
@error_handler
def get_city_by_id(id: int):
    with Session(engine) as session:
        cities = session.exec(select(Cities).where(Cities.id == id)).first()

        return cities


# cost center


@app.get("/cost-center", dependencies=[Depends(verify_token)])
@error_handler
def get_cost_center():
    return handle_get_cost_center()


@app.get("/cost-center/{id}", dependencies=[Depends(verify_token)])
@error_handler
def get_cost_center_by_id(id: int):
    return handle_get_cost_center_by_id(id)


@app.post("/cost-center", dependencies=[Depends(verify_token)])
@error_handler
def post_cost_center(cost_center_input: CostCenter):
    return handle_post_cost_center(cost_center_input)


@app.put("/cost-center/{id}", dependencies=[Depends(verify_token)])
@error_handler
def put_cost_center(id: int, cost_center_input: CostCenter):
    return handle_put_cost_center(id, cost_center_input)


@app.delete("/cost-center/{id}", dependencies=[Depends(verify_token)])
@error_handler
def delete_cost_center(id: int):
    return handle_delete_cost_center(id)


# cost center logs


@app.get("/subsidiaries/{id}/logs/costs-centers")
@error_handler
def get_cost_center_logs(id: int):
    return handle_get_cost_center_logs(id)


@app.post("/subsidiaries/{id}/logs/costs-centers", dependencies=[Depends(verify_token)])
@error_handler
def post_cost_center_logs(id: int, cost_center_log: CostCenterLogs):
    return handle_post_cost_center_logs(id, cost_center_log)


# department


@app.get("/departments", dependencies=[Depends(verify_token)])
@error_handler
def get_departments():
    return handle_get_departments()


@app.get("/departments/{id}", dependencies=[Depends(verify_token)])
@error_handler
def get_department_by_id(id: int):
    return handle_get_department_by_id(id)


@app.post("/departments", dependencies=[Depends(verify_token)])
@error_handler
def post_department(department_input: Department):
    return handle_post_department(department_input)


@app.put("/departments/{id}", dependencies=[Depends(verify_token)])
@error_handler
def put_department(id: int, department_input: Department):
    return handle_put_department(id, department_input)


@app.delete("/departments/{id}", dependencies=[Depends(verify_token)])
@error_handler
def delete_department(id: int):
    return handle_delete_department(id)


# department logs


@app.get("/subsidiaries/{id}/logs/departments", dependencies=[Depends(verify_token)])
@error_handler
def get_departments_logs(id: int):
    return handle_get_departments_logs(id)


@app.post("/subsidiaries/{id}/logs/departments", dependencies=[Depends(verify_token)])
@error_handler
def post_departments_logs(id: int, department_logs_input: DepartmentsLogs):
    return handle_post_departments_logs(id, department_logs_input)


# resignable reasons


@app.get("/resignable-reasons", dependencies=[Depends(verify_token)])
@error_handler
def get_resignable_reasons():
    return handle_get_resignable_reasons()


# resignable reasons reports


@app.post("/resignable-reasons/report", dependencies=[Depends(verify_token)])
@error_handler
def get_resignable_reasons_report(input: StatusResignableReasonsInput):
    return handle_resignable_reasons_report(input)


# neighborhoods


@app.get("/neighborhoods")
def get_neighborhoods():
    with Session(engine) as session:
        neighborhoods = session.exec(select(Neighborhoods)).all()

        return neighborhoods


@app.get("/neighborhoods/{id}")
def get_neighborhood_by_id(id: int):
    with Session(engine) as session:
        neighborhood = session.get(Neighborhoods, id)

        return neighborhood


@app.post("/neighborhoods")
def post_neighborhood(neighborhood: Neighborhoods):
    with Session(engine) as session:
        session.add(neighborhood)

        session.commit()

        session.refresh(neighborhood)

        return neighborhood


@app.put("/neighborhoods/{id}")
def put_neighborhood(id: int, neighborhood: Neighborhoods):
    with Session(engine) as session:
        db_neighborhood = session.exec(
            select(Neighborhoods).where(Neighborhoods.id == id)
        ).one()

        if neighborhood is not None and neighborhood.name != db_neighborhood.name:
            db_neighborhood.name = neighborhood.name

        session.add(db_neighborhood)

        session.commit()

        session.refresh(db_neighborhood)

        return db_neighborhood


@app.delete("/neighborhoods/{neighborhood_id}")
def delete_neighborhood(neighborhood_id: int):
    with Session(engine) as session:
        neighborhood = session.get(Neighborhoods, neighborhood_id)

        session.delete(neighborhood)

        session.commit()

        return {"message": "Neighborhood deleted successfully"}


# applicants


@app.get("/applicants")
def get_applicants():
    return handle_get_applicants()


@app.post("/applicants")
def post_applicant(applicant: Applicants):
    return handle_post_applicant(applicant)


# worker first review


@app.get("/workers/{id}/first-review")
def get_worker_first_review(id: int):
    with Session(engine) as session:
        db_worker_first_review = session.exec(
            select(WorkersFirstReview).where(WorkersFirstReview.worker_id == id)
        ).one()

        return db_worker_first_review


@app.post("/workers/{id}/first-review")
def post_worker_first_review(id: int, worker_first_review: WorkersFirstReview):
    worker_first_review.worker_id = id

    with Session(engine) as session:
        session.add(worker_first_review)

        session.commit()

        session.refresh(worker_first_review)

        return worker_first_review


# worker second review


@app.get("/workers/{id}/second-review")
def get_worker_first_review(id: int):
    with Session(engine) as session:
        db_worker_first_review = session.exec(
            select(WorkersSecondReview).where(WorkersSecondReview.worker_id == id)
        ).one()

        return db_worker_first_review


@app.post("/workers/{id}/second-review")
def post_worker_first_review(id: int, worker_second_review: WorkersSecondReview):
    worker_second_review.worker_id = id

    with Session(engine) as session:
        session.add(worker_second_review)

        session.commit()

        session.refresh(worker_second_review)

        return worker_second_review


@app.get(
    "/subsidiaries/{subsidiarie_id}/workers/functions/{function_id}/turns/{turn_id}"
)
def get_workers_by_functions(subsidiarie_id: int, function_id: int, turn_id: int):
    with Session(engine) as session:
        workers_by_function = session.exec(
            select(
                Workers.enrolment.label("enrolment"),
                Workers.name.label("name"),
                CostCenter.name.label("cost_center"),
                Department.name.label("department"),
            )
            .join(CostCenter, Workers.cost_center_id == CostCenter.id)
            .join(Department, Workers.department_id == Department.id)
            .where(Workers.subsidiarie_id == subsidiarie_id)
            .where(Workers.is_active == True)
            .where(Workers.function_id == function_id)
            .where(Workers.turn_id == turn_id)
        ).all()

        return [
            {
                "enrolment": worker.enrolment,
                "name": worker.name,
                "cost_center": worker.cost_center,
                "department": worker.department,
            }
            for worker in workers_by_function
        ]


from datetime import datetime

from dateutil.relativedelta import relativedelta
from fastapi import FastAPI
from sqlmodel import Session, select


@app.get("/subsidiaries/{subsidiarie_id}/workers/experience-time-no-first-review")
def get_workers_without_first_review_in_range(subsidiarie_id: int):
    with Session(engine) as session:
        today = datetime.today()

        start_of_week = today - relativedelta(days=today.weekday())

        end_of_week = start_of_week + relativedelta(days=6)

        start_of_week_str = start_of_week.strftime("%Y-%m-%d")

        end_of_week_str = end_of_week.strftime("%Y-%m-%d")

        workers_without_first_review = session.exec(
            select(Workers)
            .where(Workers.subsidiarie_id == subsidiarie_id)
            .where(Workers.first_review_date >= start_of_week_str)
            .where(Workers.first_review_date <= end_of_week_str)
            .where(
                ~Workers.id.in_(
                    select(WorkersFirstReview.worker_id).where(
                        WorkersFirstReview.worker_id == Workers.id
                    )
                )
            )
        ).all()

        return {
            "workers": workers_without_first_review,
            "start_of_week": start_of_week,
            "end_of_week": end_of_week,
        }


@app.get("/subsidiaries/{subsidiarie_id}/workers/experience-time-no-second-review")
def get_workers_without_second_review_in_range(subsidiarie_id: int):
    with Session(engine) as session:
        today = datetime.today()

        start_of_week = today - timedelta(days=today.weekday())

        end_of_week = start_of_week + timedelta(days=6)

        start_of_week_str = start_of_week.strftime("%Y-%m-%d")

        end_of_week_str = end_of_week.strftime("%Y-%m-%d")

        workers_without_second_review = session.exec(
            select(Workers)
            .where(Workers.subsidiarie_id == subsidiarie_id)
            .where(Workers.second_review_date >= start_of_week_str)
            .where(Workers.second_review_date <= end_of_week_str)
            .where(
                ~Workers.id.in_(
                    select(WorkersSecondReview.worker_id).where(
                        WorkersSecondReview.worker_id == Workers.id
                    )
                )
            )
        ).all()

        return {
            "workers": workers_without_second_review,
            "start_of_week": start_of_week,
            "end_of_week": end_of_week,
        }


@app.get("/subsidiaries/{subsidiarie_id}/workers/{worker_id}")
def sla(subsidiarie_id: int, worker_id: int):
    today = datetime.today().date()

    with Session(engine) as session:
        first_review = session.exec(
            select(Workers)
            .where(Workers.subsidiarie_id == subsidiarie_id)
            .where(Workers.id == worker_id)
            .where(Workers.first_review_date >= today)
        ).first()

        can_open_first_review_modal = (
            True
            if session.exec(
                select(Workers)
                .where(Workers.subsidiarie_id == subsidiarie_id)
                .where(Workers.id == worker_id)
                .where(Workers.first_review_date >= today)
            ).first()
            else False
        )

        second_review = session.exec(
            select(Workers)
            .where(Workers.subsidiarie_id == subsidiarie_id)
            .where(Workers.id == worker_id)
            .where(Workers.second_review_date >= today)
        ).first()

        can_open_second_review_modal = (
            True
            if session.exec(
                select(Workers)
                .where(Workers.subsidiarie_id == subsidiarie_id)
                .where(Workers.id == worker_id)
                .where(Workers.second_review_date >= today)
            ).first()
            else False
        )

        return {
            "first_review": first_review,
            "second_review": second_review,
            "can_open_first_review_modal": can_open_first_review_modal,
            "can_open_second_review_modal": can_open_second_review_modal,
        }


from pydantic import BaseModel


class WorkersFieldsByTurnAndFunctionInput(BaseModel):
    fields: list


@app.post(
    "/subsidiaries/{subsidiarie_id}/workers/functions/{function_id}/turns/{turn_id}"
)
def workers_fields_by_turn_and_function(
    subsidiarie_id: int,
    function_id: int,
    turn_id: int,
    input: WorkersFieldsByTurnAndFunctionInput,
):
    with Session(engine) as session:
        workers = session.exec(
            select(Workers, Function, Turn, CostCenter, Department)
            .join(Function, Workers.function_id == Function.id)
            .join(Turn, Workers.turn_id == Turn.id)
            .join(CostCenter, Workers.cost_center_id == CostCenter.id)
            .join(Department, Workers.department_id == Department.id)
            .where(Workers.subsidiarie_id == subsidiarie_id)
            .where(Workers.function_id == function_id)
            .where(Workers.turn_id == turn_id)
        ).all()

        result = [
            {
                "esocial": worker.esocial,
                "enrolment": worker.enrolment,
                "sales_code": worker.sales_code,
                "timecode": worker.timecode,
                "worker_name": worker.name,
                "function_name": function.name,
                "turn_name": turn.name,
                "cost_center_name": cost_center.name,
                "department_name": department.name,
                "admission_date": worker.admission_date,
            }
            for worker, function, turn, cost_center, department in workers
        ]

        return result

        # if not workers:
        #     return []

        # valid_fields = {column.name for column in Workers.__table__.columns}

        # requested_fields = [field for field in input.fields if field in valid_fields]

        # result = [
        #     {field: getattr(worker, field) for field in requested_fields}
        #     for worker in workers
        # ]

        # return workers


from datetime import date


@app.get("/subsidiaries/{id}/get-nr20-list")
def get_nr_list_by_subsidiarie(id: int):
    today = date.today()

    first_day = today.replace(day=1)

    last_day = today.replace(day=1).replace(month=today.month + 1) - timedelta(days=1)

    with Session(engine) as session:
        nr_list = session.exec(
            select(Workers)
            .where(Workers.subsidiarie_id == id)
            .where(Workers.second_review_date.between(first_day, last_day))
        ).all()

        return {"nr_list": nr_list, "first_day": first_day, "last_day": last_day}


# dates events


@app.get("/subsidiaries/{id}/dates-events")
def get_date_event(id: int):
    with Session(engine) as session:
        today = date.today()

        first_day = today.replace(day=1)

        last_day = today.replace(day=1).replace(month=today.month + 1) - timedelta(
            days=1
        )

        date_event = session.exec(
            select(DatesEvents)
            .where(DatesEvents.subsidiarie_id == id)
            .where(DatesEvents.date.between(first_day, last_day))
        ).all()

        return date_event


@app.get("/subsidiaries/{id}/dates/{date}/dates-events")
def get_events_by_date(id: int, date: str):
    with Session(engine) as session:
        dates_events = session.exec(
            select(DatesEvents)
            .where(DatesEvents.subsidiarie_id == id)
            .where(DatesEvents.date == date)
        ).all()

        return dates_events


@app.post("/subsidiaries/{id}/dates-events")
def post_date_event(id: int, date_event: DatesEvents):
    date_event.subsidiarie_id = id

    with Session(engine) as session:
        session.add(date_event)

        session.commit()

        session.refresh(date_event)

        return date_event


@app.delete("/subsidiaries/{subsidiarie_id}/dates-events/{event_id}")
def delete_date_event(subsidiarie_id: int, event_id: int):
    with Session(engine) as session:
        date_event = session.exec(
            select(DatesEvents)
            .where(DatesEvents.id == event_id)
            .where(DatesEvents.subsidiarie_id == subsidiarie_id)
        ).first()

        session.delete(date_event)

        session.commit()

        return {"success": True}


# genders


@app.get("/genders")
def get_genders():
    with Session(engine) as session:
        genders = session.exec(select(Genders)).all()

        return genders


# civil status


@app.get("/civil-status")
def get_civil_status():
    with Session(engine) as session:
        civil_status = session.exec(select(CivilStatus)).all()

        return civil_status


@app.get("/cities/{id}/neighborhoods")
def get_neighborhoods_by_city(id: int):
    with Session(engine) as session:
        neighborhoods = session.exec(
            select(Neighborhoods).where(Neighborhoods.city_id == id)
        ).all()

        return neighborhoods


@app.get("/ethnicities")
def get_ethnicities():
    with Session(engine) as session:
        ethnicities = session.exec(select(Ethnicity)).all()

        return ethnicities


@app.get("/get-nr-workers")
def get_nr_workers():
    with Session(engine) as session:
        nr_workers = session.exec(select(Workers).where(Workers.second_review_date))


# away reasons


@app.get("/away-reasons")
def get_away_reasons():
    with Session(engine) as session:
        get_away_reasons = select(AwayReasons)

        away_reasons = session.exec(get_away_reasons).all()

        return away_reasons


# workers


class WorkersAway(BaseModel):
    away_start_date: str
    away_end_date: str
    away_reason_id: int


@app.put("/subsidiaries/{subsidiarie_id}/workers/{worker_id}/away")
def worker_away(subsidiarie_id: int, worker_id: int, worker: WorkersAway):
    with Session(engine) as session:
        get_db_worker = (
            select(Workers)
            .where(Workers.id == worker_id)
            .where(Workers.subsidiarie_id == subsidiarie_id)
        )

        db_worker = session.exec(get_db_worker).first()

        db_worker.is_away = True

        db_worker.away_start_date = (
            worker.away_start_date
            if worker.away_start_date
            else db_worker.away_start_date
        )

        db_worker.away_end_date = (
            worker.away_end_date if worker.away_end_date else db_worker.away_end_date
        )

        db_worker.away_reason_id = (
            worker.away_reason_id if worker.away_reason_id else db_worker.away_reason_id
        )

        start_date = datetime.strptime(worker.away_start_date, "%Y-%m-%d").date()

        end_date = datetime.strptime(worker.away_end_date, "%Y-%m-%d").date()

        away_days = (end_date - start_date).days + 1

        db_worker.time_away = away_days

        session.add(db_worker)

        session.commit()

        session.refresh(db_worker)

        return db_worker


@app.put("/subsidiaries/{subsidiarie_id}/workers/{worker_id}/away-return")
def sla(subsidiarie_id: int, worker_id: int):
    with Session(engine) as session:
        get_db_worker = (
            select(Workers)
            .where(Workers.id == worker_id)
            .where(Workers.subsidiarie_id == subsidiarie_id)
        )

        db_worker = session.exec(get_db_worker).first()

        db_worker.is_away = False

        session.add(db_worker)

        session.commit()

        return db_worker


# school levels


@app.get("/school-levels")
def get_school_levels():
    return handle_get_school_levels()


# banks


@app.get("/banks")
def get_banks():
    return handle_get_banks()


class WorkersByTurnAndFunctionModel(BaseModel):
    turns: list
    functions: list


@app.post("/subsidiaries/{subsidiarie_id}/workers-by-turn-and-function")
def get_workers_by_turn_and_function(
    subsidiarie_id: int, data: WorkersByTurnAndFunctionModel
):
    with Session(engine) as session:
        result = []

        turns = data.turns

        functions = data.functions

        for turn in turns:
            for function in functions:
                workers = session.exec(
                    select(Workers)
                    .where(Workers.subsidiarie_id == subsidiarie_id)
                    .where(Workers.turn_id == turn)
                    .where(Workers.function_id == function)
                ).all()

                result.extend(workers)

        return result


# nationalities


@app.get("/nationalities", dependencies=[Depends(verify_token)])
def get_nationalities():
    return handle_get_nationalities()


@app.post("/nationalities", dependencies=[Depends(verify_token)])
def post_nationalities(nationalitie: Nationalities):
    return handle_post_nationalities(nationalitie)


@app.put("/nationalities/{id}", dependencies=[Depends(verify_token)])
def put_nationalities(id: int, nationalitie: Nationalities):
    return handle_put_nationalities(id, nationalitie)


@app.delete("/nationalities/{id}", dependencies=[Depends(verify_token)])
def delete_nationalities(id: int):
    return handle_delete_nationalities(id)


# states


@app.get("/states", dependencies=[Depends(verify_token)])
def get_states():
    return handle_get_states()


@app.get("/states/{id}", dependencies=[Depends(verify_token)])
def get_states_by_id(id: int):
    return handle_get_states_by_id(id)


@app.get("/nationalities/{id}/states", dependencies=[Depends(verify_token)])
def get_states_by_nationalitie(id: int):
    return handle_get_states_by_nationalitie(id)


@app.post("/states", dependencies=[Depends(verify_token)])
def post_states(state: States):
    return handle_post_states(state)


@app.put("/states/{id}", dependencies=[Depends(verify_token)])
def put_states(id: int, state: States):
    return handle_put_states(id, state)


@app.delete("/states/{id}")
def delete_states(id: int):
    return handle_delete_states(id)


# parents type


@app.get("/parents-type")
def get_parents_type():
    return handle_get_parents_type()


# workers parents


@app.get("/workers/{id}/parents")
def get_workers_parents(id: int):
    return handle_get_workers_parents(id)


@app.post("/workers-parents")
def post_workers_parents(worker_parent: WorkersParents):
    return handle_post_workers_parents(worker_parent)


@app.delete("/workers-parents/{id}")
def delete_workers_parents(id: int):
    return handle_delete_workers_parents(id)


# hierarchy structure


@app.get("/hierarchy-structure")
def get_hierarchy_structure():
    return handle_get_hierarchy_structure()


# wage payment method


@app.get("/wage-payment-methods")
def get_wage_payment_method():
    return handle_get_wage_payment_method()


# hollidays scale


@app.get("/subsidiaries/{id}/hollidays-scale/{date}")
def get_hollidays_scale(id: int, date: str):
    return handle_get_hollidays_scale(id, date)


@app.post("/hollidays-scale")
def post_hollidays_scale(holliday_scale: HollidaysScale):
    return handle_post_hollidays_scale(holliday_scale)


@app.delete("/hollidays-scale/{id}")
def delete_hollidays_scale(id: int):
    return handle_delete_hollidays_scale(id)


# cnh categories


@app.get("/cnh-categories")
def get_cnh_categories():
    return handle_get_cnh_categories()


@app.delete("/workers/{id}")
def delete_workers(id: int):
    with Session(engine) as session:
        worker = session.exec(select(Workers).where(Workers.id == id)).first()

        session.delete(worker)

        session.commit()

        return {"success": True}


@app.get("/functions/{id}")
def get_function_by_id(id: int):
    with Session(engine) as session:
        function = session.exec(select(Function).where(Function.id == id)).first()

        return function


import httpx


async def get_state_by_city_name(city_name: str) -> str:
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro ao acessar a API do IBGE")

    cities_data = response.json()

    for city in cities_data:
        if city["nome"].lower() == city_name.lower():
            return city["microrregiao"]["mesorregiao"]["UF"]["sigla"]

    raise HTTPException(status_code=404, detail="Cidade não encontrada na API do IBGE")


class PostCitiesInput(BaseModel):
    name: str


@app.post("/cities")
async def post_cities(city: PostCitiesInput):
    with Session(engine) as session:
        result = await get_state_by_city_name(city.name)

        new_city_state_id = session.exec(
            select(States.id).where(States.sail == result)
        ).first()

        new_city = Cities(name=city.name, state_id=new_city_state_id)

        session.add(new_city)

        session.commit()

        session.refresh(new_city)

        cities_list = session.exec(select(Cities)).all()

        return cities_list


import requests


def get_city_by_neighborhood(bairro: str) -> str:
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": f"{bairro}, Brasil",
        "format": "json",
        "addressdetails": 1,
        "limit": 1,
    }

    headers = {"User-Agent": "MinhaAplicacao/1.0"}

    response = requests.get(url, params=params, headers=headers)

    data = response.json()

    if not data:
        return "Cidade não encontrada"

    address = data[0].get("address", {})

    return (
        address.get("city")
        or address.get("town")
        or address.get("village", "Cidade não identificada")
    )


class PostNeighborhoodsInput(BaseModel):
    name: str


@app.post("/news")
def post_cities(neighborhood: PostNeighborhoodsInput):
    with Session(engine) as session:
        new_neighborhood_city_name = get_city_by_neighborhood(neighborhood.name)

        new_neighborhood_city_id = session.exec(
            select(Cities.id).where(Cities.name == new_neighborhood_city_name)
        ).first()

        new_neighborhood = Neighborhoods(
            name=neighborhood.name, city_id=new_neighborhood_city_id
        )

        session.add(new_neighborhood)

        session.commit()

        session.refresh(new_neighborhood)

        all_neighborhoods = session.exec(select(Neighborhoods)).all()

        return all_neighborhoods


# all subsidiaries no first review and second review


@app.post("/subsidiaries/workers/experience-time-no-first-review")
async def get_workers_without_first_review_in_range_all(data: SubsidiaryFilter):
    return await handle_get_workers_without_first_review_in_range_all(data)


@app.post("/subsidiaries/workers/experience-time-no-second-review")
async def get_workers_without_second_review_in_range_all(data: SubsidiaryFilter):
    return await handle_get_workers_without_second_review_in_range_all(data)


from sqlalchemy import and_


@app.post("/subsidiaries/away-workers")
def get_away_return_workers(data: SubsidiaryFilter):
    today = date.today()

    start_of_week = today - timedelta(days=today.weekday())

    end_of_week = start_of_week + timedelta(days=6)

    with Session(engine) as session:
        workers_away_return = session.exec(
            select(Workers).where(
                and_(
                    Workers.subsidiarie_id.in_(data.subsidiaries_ids),
                    Workers.is_away.is_(True),
                    Workers.away_end_date >= start_of_week,
                    Workers.away_end_date <= end_of_week,
                )
            )
        ).all()

    return {
        "workers": workers_away_return,
        "start_of_week": start_of_week,
        "end_of_week": end_of_week,
    }
