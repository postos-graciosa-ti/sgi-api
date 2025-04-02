import threading
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, UploadFile
from sqlmodel import Session, select

from controllers.candidates import (
    handle_get_candidates,
    handle_get_candidates_by_status,
    handle_post_candidate,
)
from controllers.cities_states import (
    handle_get_cities,
    handle_get_city_by_id,
    handle_get_states,
    handle_get_states_by_id,
)
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
from controllers.jobs import (
    handle_delete_job,
    handle_get_jobs,
    handle_get_jobs_by_subsidiarie_id,
    handle_post_job,
)
from controllers.months import handle_get_months
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
from database.sqlite import engine
from functions.auth import verify_token
from functions.error_handling import error_handler
from keep_alive import keep_alive_function
from middlewares.cors_middleware import add_cors_middleware
from models.applicants import Applicants
from models.candidate import Candidate
from models.cities import Cities
from models.civil_status import CivilStatus
from models.cost_center import CostCenter
from models.cost_center_logs import CostCenterLogs
from models.dates_events import DatesEvents
from models.department import Department
from models.department_logs import DepartmentsLogs
from models.ethnicity import Ethnicity
from models.function import Function
from models.function_logs import FunctionLogs
from models.genders import Genders
from models.jobs import Jobs
from models.neighborhoods import Neighborhoods
from models.role import Role
from models.scale_logs import ScaleLogs
from models.states import States
from models.subsidiarie import Subsidiarie
from models.subsidiarie_logs import SubsidiarieLogs
from models.turn import Turn
from models.TurnsLogs import TurnsLogs
from models.user import User
from models.users_logs import UsersLogs
from models.workers import Workers
from models.workers_first_review import WorkersFirstReview
from models.workers_logs import WorkersLogs
from models.workers_second_review import WorkersSecondReview
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


@app.get("/workers/subsidiarie/{subsidiarie_id}")
def get_workers_by_subsidiarie(subsidiarie_id: int):
    return handle_get_workers_by_subsidiarie(subsidiarie_id)


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
    if isinstance(worker.admission_date, str):
        admission_date = datetime.strptime(worker.admission_date, "%Y-%m-%d")
    else:
        admission_date = worker.admission_date

    # Adicionando meses corretamente
    worker.first_review_date = admission_date + relativedelta(months=1)
    worker.second_review_date = admission_date + relativedelta(months=2)

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


# states


@app.get("/states", dependencies=[Depends(verify_token)])
@error_handler
def get_states():
    with Session(engine) as session:
        states = session.exec(select(States)).all()

        return states


@app.get("/states/{id}", dependencies=[Depends(verify_token)])
@error_handler
def get_states_by_id(id: int):
    return handle_get_states_by_id(id)


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
    return handle_get_city_by_id(id)


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


@app.get("/applicants")
def get_applicant():
    with Session(engine) as session:
        applicants = session.exec(select(Applicants)).all()

        return applicants


@app.post("/applicants")
def post_applicant(applicant: Applicants):
    with Session(engine) as session:
        session.add(applicant)

        session.commit()

        session.refresh(applicant)

        return applicant


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

        # Obtém o início da semana (segunda-feira)
        start_of_week = today - relativedelta(days=today.weekday())

        # Obtém o final da semana (domingo)
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

        return workers_without_first_review


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

        return workers_without_second_review


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
