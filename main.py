import json
import threading
from calendar import monthrange
from datetime import date, datetime, timedelta

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy import inspect
from sqlalchemy.exc import OperationalError
from sqlalchemy_utils import database_exists
from sqlmodel import Session, and_, select

from controllers.candidates import (
    handle_get_candidates,
    handle_get_candidates_by_status,
    handle_post_candidate,
)
from controllers.candidato import (
    handle_delete_candidato,
    handle_get_candidato,
    handle_get_candidato_by_id,
    handle_post_candidato,
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
    handle_get_subsidiarie_scale_to_print,
    handle_handle_scale,
    handle_post_scale,
    handle_post_some_workers_scale,
)
from controllers.scales_logs import (
    handle_get_scales_logs,
    handle_get_subsidiarie_scales_logs,
    handle_post_scale_logs,
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
    handle_put_subsidiarie,
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
)
from database.sqlite import create_db_and_tables, engine
from functions.auth import verify_token
from functions.handle_operation import handle_database_operation
from keep_alive import keep_alive_function
from middlewares.cors_middleware import add_cors_middleware
from models.candidate import Candidate
from models.candidato import Candidato
from models.cost_center import CostCenter
from models.cost_center_logs import CostCenterLogs
from models.department import Department
from models.department_logs import DepartmentsLogs
from models.function import Function
from models.function_logs import FunctionLogs
from models.jobs import Jobs
from models.resignable_reasons import ResignableReasons
from models.role import Role
from models.scale import Scale
from models.scale_logs import ScaleLogs
from models.subsidiarie import Subsidiarie
from models.subsidiarie_logs import SubsidiarieLogs
from models.turn import Turn
from models.TurnsLogs import TurnsLogs
from models.user import User
from models.users_logs import UsersLogs
from models.workers import Workers
from models.workers_logs import WorkersLogs
from models.workers_logs_create import WorkersLogsCreate
from models.workers_logs_delete import WorkersLogsDelete
from models.workers_logs_update import WorkersLogsUpdate
from models.workers_notations import WorkersNotations
from pyhints.resignable_reasons import StatusResignableReasonsInput
from pyhints.scales import (
    PostScaleInput,
    PostSomeWorkersScaleInput,
    ScalesReportInput,
    WorkerDeactivateInput,
)
from pyhints.subsidiaries import PutSubsidiarie
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
from seeds.seed_all import seed_database

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


@app.post("/subsidiaries/{id}/scripts/excel-scraping")
async def excel_scraping(id: int, file: UploadFile = File(...)):
    return await handle_excel_scraping(id, file)


# users


@app.get("/users")
def get_users(token: dict = Depends(verify_token)):
    with Session(engine) as session:
        users = (
            session.exec(select(User, Role).join(Role, User.role_id == Role.id))
            .tuples()
            .all()
        )

        result = []

        for user, role in users:
            result.append(
                {
                    "user_id": user.id,
                    "user_email": user.email,
                    "user_name": user.name,
                    "user_subsidiaries": [
                        session.get(Subsidiarie, id)
                        for id in user.subsidiaries_id
                        if id is not None and session.get(Subsidiarie, id) is not None
                    ],
                    "role_id": role.id,
                    "role_name": role.name,
                }
            )

    return result


@app.get("/users/{id}")
def get_user_by_id(id: int, token: dict = Depends(verify_token)):
    return handle_get_user_by_id(id)


@app.get("/users_roles")
def get_users_roles(token: dict = Depends(verify_token)):
    return handle_get_users_roles()


@app.post("/users")
def post_user(user: User, token: dict = Depends(verify_token)):
    return handle_post_user(user)


@app.put("/users/{id}")
def put_user(id: int, user: User, token: dict = Depends(verify_token)):
    return handle_put_user(id, user)


@app.delete("/users/{id}")
def delete_user(id: int, token: dict = Depends(verify_token)):
    return handle_delete_user(id)


@app.post("/test")
def test(arr: Test, token: dict = Depends(verify_token)):
    return handle_get_test(arr)


@app.post("/users/create-password")
def create_user_password(
    userData: CreateUserPasswordInput, token: dict = Depends(verify_token)
):
    return handle_create_user_password(userData)


@app.post("/confirm-password")
def confirm_password(userData: ConfirmPassword, token: dict = Depends(verify_token)):
    return handle_confirm_password(userData)


@app.post("/users/change-password")
def change_password(
    userData: ChangeUserPasswordInput, token: dict = Depends(verify_token)
):
    return handle_change_password(userData)


# user logs


@app.get("/logs/users")
def get_logs_user():
    return handle_get_logs_user()


@app.post("/logs/users")
def post_logs_user(users_logs: UsersLogs):
    return handle_post_logs_user(users_logs)


# months


@app.get("/months")
def get_months(token: dict = Depends(verify_token)):
    return handle_get_months()


# subsidiaries


@app.get("/subsidiaries")
def get_subsidiaries(token: dict = Depends(verify_token)):
    return handle_get_subsidiaries()


@app.get("/subsidiaries/{id}")
def get_subsidiarie_by_id(id: int, token: dict = Depends(verify_token)):
    return handle_get_subsidiarie_by_id(id)


@app.post("/subsidiaries")
def post_subsidiaries(formData: Subsidiarie, token: dict = Depends(verify_token)):
    return handle_post_subsidiaries(formData)


@app.put("/subsidiaries/{id}")
def put_subsidiaries(
    id: int, formData: PutSubsidiarie, token: dict = Depends(verify_token)
):
    return handle_put_subsidiarie(id, formData)


@app.delete("/subsidiaries/{id}")
def delete_subsidiaries(id: int, token: dict = Depends(verify_token)):
    return handle_delete_subsidiarie(id)


# subsidiaries notifications


@app.get("/subsidiaries/{id}/notifications")
async def get_subsidiarie_notifications(id: int, token: dict = Depends(verify_token)):
    return await handle_get_subsidiarie_notifications(id)


@app.get("/subsidiaries/{id}/workers-status")
async def get_subsidiaries_status(id: int, token: dict = Depends(verify_token)):
    return await handle_database_operation(handle_get_subsidiaries_status, id)


# subsidiaries logs


@app.get("/subsidiaries-logs")
async def get_subsidiarie_logs():
    return await handle_get_subsidiarie_logs()


@app.post("/subsidiaries/logs")
async def post_subsidiaries_logs(subsidiarie_log: SubsidiarieLogs):
    return await handle_post_subsidiaries_logs(subsidiarie_log)


# turns


@app.get("/subsidiaries/{id}/turns")
def get_subsidiarie_turns(id: int):
    return handle_get_subsidiarie_turns(id)


@app.get("/turns")
def get_turns(token: dict = Depends(verify_token)):
    return handle_get_turns()


@app.get("/turns/{id}")
async def get_turn_by_id(id: int, token: dict = Depends(verify_token)):
    return await handle_database_operation(handle_get_turn_by_id, id)


@app.post("/turns")
def post_turns(formData: Turn, token: dict = Depends(verify_token)):
    return handle_post_turns(formData)


@app.put("/turns/{id}")
def put_turn(id: int, formData: PutTurn, token: dict = Depends(verify_token)):
    return handle_put_turn(id, formData)


@app.delete("/turns/{id}")
def delete_turn(id: int, token: dict = Depends(verify_token)):
    return handle_delete_turn(id)


# turns logs


@app.get("/subsidiaries/{id}/logs/turns")
async def get_turns_logs(id: int):
    return await handle_database_operation(handle_get_turns_logs, id)


@app.post("/subsidiaries/{id}/logs/turns")
async def post_turns_logs(id: int, turn_log: TurnsLogs):
    return await handle_post_turns_logs(id, turn_log)


# workers


@app.get("/workers/{id}")
async def get_worker_by_id(id: int, token: dict = Depends(verify_token)):
    return await handle_database_operation(handle_get_worker_by_id, id)


@app.get("/workers/turns/{turn_id}/subsidiarie/{subsidiarie_id}")
def get_workers_by_turn_and_subsidiarie(
    turn_id: int, subsidiarie_id: int, token: dict = Depends(verify_token)
):
    return handle_get_workers_by_turn_and_subsidiarie(turn_id, subsidiarie_id)


@app.get("/workers/on-track/turn/{turn_id}/subsidiarie/{subsidiarie_id}")
def get_active_workers_by_turn_and_subsidiarie(
    turn_id: int, subsidiarie_id: int, token: dict = Depends(verify_token)
):
    return handle_get_active_workers_by_turn_and_subsidiarie(turn_id, subsidiarie_id)


@app.get("/workers/active/subsidiarie/{subsidiarie_id}/function/{function_id}")
def get_active_workers_by_subsidiarie_and_function(
    subsidiarie_id: int, function_id: int, token: dict = Depends(verify_token)
):
    return handle_get_active_workers_by_subsidiarie_and_function(
        subsidiarie_id, function_id
    )


@app.get("/workers/subsidiarie/{subsidiarie_id}")
def get_workers_by_subsidiarie(
    subsidiarie_id: int, token: dict = Depends(verify_token)
):
    return handle_get_workers_by_subsidiarie(subsidiarie_id)


@app.get(
    "/workers/subsidiaries/{subsidiarie_id}/functions/{function_id}/turns/{turn_id}"
)
async def get_workers_by_subsidiaries_functions_and_turns(
    subsidiarie_id: int,
    function_id: int,
    turn_id: int,
    token: dict = Depends(verify_token),
):
    return await handle_database_operation(
        handle_get_workers_by_subsidiaries_functions_and_turns,
        subsidiarie_id,
        function_id,
        turn_id,
    )


@app.post("/workers")
async def post_worker(worker: Workers, token: dict = Depends(verify_token)):
    return await handle_database_operation(handle_post_worker, worker)


@app.put("/workers/{id}")
async def put_worker(id: int, worker: Workers, token: dict = Depends(verify_token)):
    return await handle_database_operation(handle_put_worker, id, worker)


@app.put("/workers/{id}/deactivate")
async def deactivate_worker(
    id: int, worker: WorkerDeactivateInput, token: dict = Depends(verify_token)
):
    return await handle_database_operation(handle_deactivate_worker, id, worker)


@app.put("/workers/{id}/reactivate")
def reactivate_worker(id: int, token: dict = Depends(verify_token)):
    return handle_reactivate_worker(id)


# workers logs


@app.get("/subsidiaries/{subsidiarie_id}/workers/{worker_id}")
def get_worker_by_id_in_subsidiarie(subsidiarie_id: int, worker_id: int):
    with Session(engine) as session:
        result = session.exec(
            select(
                Workers,
                Function,
                Turn,
                CostCenter,
                Department,
            )
            .join(Function, Workers.function_id == Function.id)
            .join(Turn, Workers.turn_id == Turn.id)
            .join(CostCenter, Workers.cost_center_id == CostCenter.id)
            .where(Workers.id == worker_id)
            .where(Workers.subsidiarie_id == subsidiarie_id)
        ).first()

        worker = [
            {
                "name": result[0].name,
                "function": result[1].name,
                "turn": result[2].name,
                "cost_center": result[3].name,
                "setor": result[4].name,
            }
        ]

        return worker


@app.get("/subsidiaries/{id}/workers/logs")
def get_workers_logs(id: int):
    with Session(engine) as session:
        workers_logs = session.exec(
            select(WorkersLogs).where(WorkersLogs.subsidiarie_id == id)
        ).all()

        return workers_logs


@app.post("/subsidiaries/{id}/workers/logs")
def post_workers_logs(id: int, workers_log: WorkersLogs):
    with Session(engine) as session:
        workers_log.subsidiarie_id = id

        session.add(workers_log)

        session.commit()

        session.refresh(workers_log)

        return workers_log


# workers logs create


@app.get("/logs/subsidiaries/{id}/workers/create")
def get_create_workers_logs(id: int, token: dict = Depends(verify_token)):
    return handle_get_create_workers_logs(id)


@app.post("/logs/subsidiaries/{id}/workers/create")
def post_create_workers_logs(
    id: int, worker_log: WorkerLogCreateInput, token: dict = Depends(verify_token)
):
    return handle_post_create_workers_logs(id, worker_log)


# workers logs update


@app.get("/logs/subsidiaries/{id}/workers/update")
def get_update_workers_logs(id: int, token: dict = Depends(verify_token)):
    return handle_get_update_workers_logs(id)


@app.post("/logs/subsidiaries/{id}/workers/update")
def post_update_workers_logs(
    id: int, worker_log: WorkerLogUpdateInput, token: dict = Depends(verify_token)
):
    return handle_post_update_workers_logs(id, worker_log)


# workers logs delete


@app.get("/logs/subsidiaries/{id}/workers/delete")
def get_delete_workers_logs(id: int, token: dict = Depends(verify_token)):
    return handle_get_delete_workers_logs(id)


@app.post("/logs/subsidiaries/{id}/workers/delete")
def post_delete_workers_logs(
    id: int, worker_log: WorkerLogDeleteInput, token: dict = Depends(verify_token)
):
    return handle_post_delete_workers_logs(id, worker_log)


# workers notations


@app.get("/workers/{id}/notations")
def get_worker_notations(id: int, token: dict = Depends(verify_token)):
    return handle_get_worker_notations(id)


@app.post("/workers/{id}/notations")
def post_worker_notation(
    id: int, data: PostWorkerNotationInput, token: dict = Depends(verify_token)
):
    return handle_post_worker_notation(id, data)


@app.delete("/workers-notations/{id}")
def delete_worker_notation(id: int, token: dict = Depends(verify_token)):
    return handle_delete_worker_notation(id)


# functions


@app.get("/subsidiaries/{id}/functions")
def get_functions_by_subsidiarie(id: int, token: dict = Depends(verify_token)):
    return handle_get_functions_by_subsidiarie(id)


@app.get("/functions")
def get_functions(token: dict = Depends(verify_token)):
    return handle_get_functions()


@app.get("/functions/for-users")
def get_functions_for_users(token: dict = Depends(verify_token)):
    return handle_get_functions_for_users()


@app.get("/functions/for-workers")
def get_functions_for_users(token: dict = Depends(verify_token)):
    return handle_get_functions_for_workers()


@app.post("/functions")
def post_function(function: Function, token: dict = Depends(verify_token)):
    return handle_post_function(function)


@app.put("/functions/{id}")
def put_function(id: int, function: Function, token: dict = Depends(verify_token)):
    return handle_put_function(id, function)


@app.delete("/functions/{id}")
def delete_function(id: int, token: dict = Depends(verify_token)):
    return handle_delete_function(id)


# functions logs


@app.get("/subsidiaries/{id}/functions/logs")
def get_functions_logs(id: int):
    return handle_get_functions_logs(id)


@app.post("/subsidiaries/{id}/functions/logs")
def post_functions_logs(id: int, function_log: FunctionLogs):
    return handle_post_functions_logs(id, function_log)


# jobs


@app.get("/jobs")
def get_jobs(token: dict = Depends(verify_token)):
    return handle_get_jobs()


@app.get("/jobs/subsidiarie/{subsidiarie_id}")
def get_jobs_by_subsidiarie_id(
    subsidiarie_id: int, token: dict = Depends(verify_token)
):
    return handle_get_jobs_by_subsidiarie_id(subsidiarie_id)


@app.post("/jobs")
def post_job(job: Jobs, token: dict = Depends(verify_token)):
    return handle_post_job(job)


@app.delete("/jobs/{job_id}")
def delete_job(job_id: int, token: dict = Depends(verify_token)):
    return handle_delete_job(job_id)


# roles


@app.get("/roles")
def get_roles(token: dict = Depends(verify_token)):
    return handle_get_roles()


# candidates


@app.get("/candidates")
def get_candidates(token: dict = Depends(verify_token)):
    return handle_get_candidates()


@app.get("/candidates/status/{id}")
def get_candidates_by_status(id: int, token: dict = Depends(verify_token)):
    return handle_get_candidates_by_status(id)


@app.post("/candidates")
def post_candidate(candidate: Candidate, token: dict = Depends(verify_token)):
    return handle_post_candidate(candidate)


# scales


@app.get("/scales/subsidiaries/{subsidiarie_id}")
def get_scales_by_subsidiarie_id(subsidiarie_id: int):
    return handle_get_scales_by_subsidiarie_id(subsidiarie_id)


@app.get("/scales/subsidiaries/{subsidiarie_id}/workers/{worker_id}")
def get_scales_by_subsidiarie_and_worker_id(subsidiarie_id: int, worker_id: int):
    return handle_get_scales_by_subsidiarie_and_worker_id(subsidiarie_id, worker_id)


@app.get("/scales/day-off/quantity")
async def get_days_off_quantity():
    return await handle_database_operation(handle_get_days_off_quantity)


@app.post("/scales")
def post_scale(form_data: PostScaleInput):
    return handle_post_scale(form_data)


@app.post("/scales/some-workers")
async def post_some_workers_scale(form_data: PostSomeWorkersScaleInput):
    return await handle_database_operation(handle_post_some_workers_scale, form_data)


@app.post("/delete-scale")
def handle_scale(form_data: PostScaleInput):
    return handle_handle_scale(form_data)


@app.delete("/scales/{scale_id}/subsidiaries/{subsidiarie_id}")
def delete_scale(scale_id: int, subsidiarie_id: int):
    return handle_delete_scale(scale_id, subsidiarie_id)


# scale logs


@app.get("/subsidiaries/{id}/scales/logs")
def get_subsidiarie_scales_logs(id: int):
    return handle_get_subsidiarie_scales_logs(id)


@app.get("/logs/scales")
async def get_scales_logs(token: dict = Depends(verify_token)):
    return await handle_database_operation(handle_get_scales_logs)


@app.post("/logs/scales")
async def post_scales_logs(
    scales_logs_input: ScaleLogs, token: dict = Depends(verify_token)
):
    return await handle_database_operation(handle_post_scale_logs, scales_logs_input)


# scale reports


@app.post("/reports/subsidiaries/{subsidiarie_id}/scales/days-on")
async def generate_scale_days_on_report(
    subsidiarie_id: int, input: ScalesReportInput, token: dict = Depends(verify_token)
):
    return await handle_database_operation(
        handle_generate_scale_days_on_report, subsidiarie_id, input
    )


@app.post("/reports/subsidiaries/{subsidiarie_id}/scales/days-off")
async def generate_scale_days_off_report(
    subsidiarie_id: int, input: ScalesReportInput, token: dict = Depends(verify_token)
):
    return await handle_database_operation(
        handle_generate_scale_days_off_report, subsidiarie_id, input
    )


# scales print


@app.get("/subsidiaries/{id}/scales/print")
def get_subsidiarie_scale_to_print(id: int):
    return handle_get_subsidiarie_scale_to_print(id)


# states


@app.get("/states")
async def get_states(token: dict = Depends(verify_token)):
    return await handle_get_states()


@app.get("/states/{id}")
async def get_states_by_id(id: int, token: dict = Depends(verify_token)):
    return await handle_get_states_by_id(id)


# cities


@app.get("/cities")
async def get_cities(token: dict = Depends(verify_token)):
    return await handle_get_cities()


@app.get("/cities/{id}")
async def get_city_by_id(id: int, token: dict = Depends(verify_token)):
    return await handle_get_city_by_id(id)


# cost center


@app.get("/cost-center")
async def get_cost_center(token: dict = Depends(verify_token)):
    return await handle_database_operation(handle_get_cost_center)


@app.get("/cost-center/{id}")
async def get_cost_center_by_id(id: int, token: dict = Depends(verify_token)):
    return await handle_database_operation(handle_get_cost_center_by_id, id)


@app.post("/cost-center")
async def post_cost_center(
    cost_center_input: CostCenter, token: dict = Depends(verify_token)
):
    return await handle_database_operation(handle_post_cost_center, cost_center_input)


@app.put("/cost-center/{id}")
async def put_cost_center(
    id: int, cost_center_input: CostCenter, token: dict = Depends(verify_token)
):
    return await handle_database_operation(
        handle_put_cost_center, id, cost_center_input
    )


@app.delete("/cost-center/{id}")
async def delete_cost_center(id: int, token: dict = Depends(verify_token)):
    return await handle_database_operation(handle_delete_cost_center, id)


# cost center logs


@app.get("/subsidiaries/{id}/logs/costs-centers")
async def get_cost_center_logs(id: int):
    return await handle_database_operation(handle_get_cost_center_logs, id)


@app.post("/subsidiaries/{id}/logs/costs-centers")
async def post_cost_center_logs(id: int, cost_center_log: CostCenterLogs):
    return await handle_database_operation(
        handle_post_cost_center_logs, id, cost_center_log
    )


# department


@app.get("/departments")
async def get_departments(token: dict = Depends(verify_token)):
    return await handle_database_operation(handle_get_departments)


@app.get("/departments/{id}")
async def get_department_by_id(id: int, token: dict = Depends(verify_token)):
    return await handle_database_operation(handle_get_department_by_id, id)


@app.post("/departments")
async def post_department(
    department_input: Department, token: dict = Depends(verify_token)
):
    return await handle_database_operation(handle_post_department, department_input)


@app.put("/departments/{id}")
async def put_department(
    id: int, department_input: Department, token: dict = Depends(verify_token)
):
    return await handle_put_department(id, department_input)


@app.delete("/departments/{id}")
async def delete_department(id: int, token: dict = Depends(verify_token)):
    return await handle_delete_department(id)


# department logs


@app.get("/subsidiaries/{id}/logs/departments")
async def get_departments_logs(id: int):
    return await handle_database_operation(handle_get_departments_logs, id)


@app.post("/subsidiaries/{id}/logs/departments")
async def post_departments_logs(id: int, department_logs_input: DepartmentsLogs):
    return await handle_database_operation(
        handle_post_departments_logs, id, department_logs_input
    )


# resignable reasons


@app.get("/resignable-reasons")
async def get_resignable_reasons(token: dict = Depends(verify_token)):
    return await handle_database_operation(handle_get_resignable_reasons)


# resignable reasons reports


@app.post("/resignable-reasons/report")
async def get_resignable_reasons_report(
    input: StatusResignableReasonsInput, token: dict = Depends(verify_token)
):
    return await handle_database_operation(handle_resignable_reasons_report, input)
