from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, UploadFile
from pydantic import BaseModel
from sqlalchemy_utils import database_exists
from sqlmodel import Session

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
from controllers.departments import (
    handle_delete_department,
    handle_get_department_by_id,
    handle_get_departments,
    handle_post_department,
    handle_put_department,
)
from controllers.functions import (
    handle_delete_function,
    handle_get_functions,
    handle_get_functions_for_users,
    handle_get_functions_for_workers,
    handle_post_function,
    handle_put_function,
)
from controllers.jobs import (
    handle_delete_job,
    handle_get_jobs,
    handle_get_jobs_by_subsidiarie_id,
    handle_post_job,
)
from controllers.months import handle_get_months
from controllers.roles import handle_get_roles
from controllers.root import handle_activate_render_server, handle_get_docs_info
from controllers.scale import (
    handle_delete_scale,
    handle_get_days_off_quantity,
    handle_get_scales_by_subsidiarie_and_worker_id,
    handle_get_scales_by_subsidiarie_id,
    handle_post_scale,
    handle_post_some_workers_scale,
)
from controllers.scales_logs import handle_get_scales_logs, handle_post_scale_logs
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
from controllers.subsidiaries_notifications import (
    handle_get_subsidiarie_notifications,
    handle_get_subsidiaries_status,
)
from controllers.turn import (
    handle_delete_turn,
    handle_get_turn_by_id,
    handle_get_turns,
    handle_post_turns,
    handle_put_turn,
)
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
from controllers.workers import (
    handle_deactivate_worker,
    handle_get_active_workers_by_subsidiarie_and_function,
    handle_get_active_workers_by_turn_and_subsidiarie,
    handle_get_worker_by_id,
    handle_get_workers_by_subsidiarie,
    handle_get_workers_by_subsidiaries_functions_and_turns,
    handle_get_workers_by_turn_and_subsidiarie,
    handle_post_worker,
    handle_put_worker,
)
from database.sqlite import create_db_and_tables, engine
from functions.auth import verify_token
from functions.handle_operation import handle_database_operation
from middlewares.cors_middleware import add_cors_middleware
from models.candidate import Candidate
from models.candidato import Candidato
from models.cost_center import CostCenter
from models.department import Department
from models.function import Function
from models.jobs import Jobs
from models.scale_logs import ScaleLogs
from models.subsidiarie import Subsidiarie
from models.turn import Turn
from models.user import User
from models.workers import Workers
from pyhints.scales import PostScaleInput, PostSomeWorkersScaleInput, ScalesReportInput
from pyhints.subsidiaries import PutSubsidiarie
from pyhints.turns import PutTurn
from pyhints.users import (
    ChangeUserPasswordInput,
    ConfirmPassword,
    CreateUserPasswordInput,
    Test,
)
from scripts.excel_scraping import handle_excel_scraping
from seeds.seed_all import seed_database

# pre settings

load_dotenv()

app = FastAPI()

add_cors_middleware(app)

# root


@app.on_event("startup")
def on_startup():
    if not database_exists(engine.url):
        create_db_and_tables()

        seed_database()


@app.get("/")
def get_docs_info():
    return handle_get_docs_info()


@app.get("/render-server/activate")
def activate_render_server():
    return handle_activate_render_server()


# candidato


@app.get("/candidato")
def get_candidato():
    return handle_get_candidato()


@app.get("/candidato/{id}")
def get_candidato_by_id(id: int):
    return handle_get_candidato_by_id(id)


@app.post("/candidato")
def post_candidato(candidato: Candidato):
    return handle_post_candidato(candidato)


@app.delete("/candidato/{id}")
def delete_candidato(id: int):
    return handle_delete_candidato(id)


# users


@app.get("/users")
def get_users(token: dict = Depends(verify_token)):
    return handle_get_users()


@app.get("/users/{id}")
def get_user_by_id(id: int):
    return handle_get_user_by_id(id)


@app.get("/users_roles")
def get_users_roles():
    return handle_get_users_roles()


@app.post("/users/login")
def user_login(user: User):
    return handle_user_login(user)


@app.post("/users")
def post_user(user: User):
    return handle_post_user(user)


@app.put("/users/{id}")
def put_user(id: int, user: User):
    return handle_put_user(id, user)


@app.delete("/users/{id}")
def delete_user(id: int):
    return handle_delete_user(id)


@app.post("/test")
def test(arr: Test):
    return handle_get_test(arr)


@app.post("/users/create-password")
def create_user_password(userData: CreateUserPasswordInput):
    return handle_create_user_password(userData)


@app.post("/confirm-password")
def confirm_password(userData: ConfirmPassword):
    return handle_confirm_password(userData)


@app.post("/users/change-password")
def change_password(userData: ChangeUserPasswordInput):
    return handle_change_password(userData)


# months


@app.get("/months")
def get_months():
    return handle_get_months()


# subsidiaries


@app.get("/subsidiaries")
def get_subsidiaries():
    return handle_get_subsidiaries()


@app.get("/subsidiaries/{id}")
def get_subsidiarie_by_id(id: int):
    return handle_get_subsidiarie_by_id(id)


@app.post("/subsidiaries")
def post_subsidiaries(formData: Subsidiarie):
    return handle_post_subsidiaries(formData)


@app.put("/subsidiaries/{id}")
def put_subsidiaries(id: int, formData: PutSubsidiarie):
    return handle_put_subsidiarie(id, formData)


@app.delete("/subsidiaries/{id}")
def delete_subsidiaries(id: int):
    return handle_delete_subsidiarie(id)


# subsidiarie notifications


@app.get("/subsidiaries/{id}/notifications")
async def get_subsidiarie_notifications(id: int):
    return await handle_get_subsidiarie_notifications(id)


@app.get("/subsidiaries/{id}/workers-status")
async def get_subsidiaries_status(id: int):
    return await handle_database_operation(handle_get_subsidiaries_status, id)


# turn


@app.get("/turns")
def get_turns():
    return handle_get_turns()


@app.get("/turns/{id}")
async def get_turn_by_id(id: int):
    return await handle_database_operation(handle_get_turn_by_id, id)


@app.post("/turns")
def post_turns(formData: Turn):
    return handle_post_turns(formData)


@app.put("/turns/{id}")
def put_turn(id: int, formData: PutTurn):
    return handle_put_turn(id, formData)


@app.delete("/turns/{id}")
def delete_turn(id: int):
    return handle_delete_turn(id)


# workers


@app.get("/workers/{id}")
async def get_worker_by_id(id: int):
    return await handle_database_operation(handle_get_worker_by_id, id)


@app.get("/workers/turns/{turn_id}/subsidiarie/{subsidiarie_id}")
def get_workers_by_turn_and_subsidiarie(turn_id: int, subsidiarie_id: int):
    return handle_get_workers_by_turn_and_subsidiarie(turn_id, subsidiarie_id)


@app.get("/workers/on-track/turn/{turn_id}/subsidiarie/{subsidiarie_id}")
def get_active_workers_by_turn_and_subsidiarie(turn_id: int, subsidiarie_id: int):
    return handle_get_active_workers_by_turn_and_subsidiarie(turn_id, subsidiarie_id)


@app.get("/workers/active/subsidiarie/{subsidiarie_id}/function/{function_id}")
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
    "/workers/subsidiaries/{subsidiarie_id}/functions/{function_id}/turns/{turn_id}"
)
async def get_workers_by_subsidiaries_functions_and_turns(
    subsidiarie_id: int, function_id: int, turn_id: int
):
    return await handle_database_operation(
        handle_get_workers_by_subsidiaries_functions_and_turns,
        subsidiarie_id,
        function_id,
        turn_id,
    )


# @app.post("/workers")
# def post_worker(worker: Workers):
#     return handle_post_worker(worker)


# @app.put("/workers/{id}")
# def put_worker(id: int, worker: Workers):
#     return handle_put_worker(id, worker)


# @app.put("/workers/deactivate/{worker_id}")
# def deactivate_worker(worker_id: int):
#     return handle_deactivate_worker(worker_id)


@app.post("/workers")
def post_worker(worker: Workers):
    with Session(engine) as session:
        session.add(worker)

        session.commit()

        session.refresh(worker)
    return worker

    # name: str = Field(index=True)
    # function_id: int = Field(default=None, foreign_key="function.id")
    # subsidiarie_id: int = Field(default=None, foreign_key="subsidiarie.id")
    # is_active: bool = Field(default=True)
    # turn_id: int = Field(default=None, foreign_key="turn.id")
    # cost_center_id: int = Field(default=None, foreign_key="costcenter.id")
    # department_id: int = Field(default=None, foreign_key="department.id")
    # # security_password: str | None = Field(default=None, nullable=True)
    # admission_date: str = Field(index=True)
    # resignation_date: str = Field(index=True)


@app.put("/workers/{id}")
def put_worker(id: int, worker: Workers):
    with Session(engine) as session:
        db_worker = session.get(Workers, id)

        db_worker.name = worker.name if worker.name else db_worker.name

        db_worker.function_id = (
            worker.function_id if worker.function_id else db_worker.function_id
        )

        db_worker.subsidiarie_id = (
            worker.subsidiarie_id if worker.subsidiarie_id else db_worker.subsidiarie_id
        )

        db_worker.is_active = (
            worker.is_active if worker.is_active is not None else db_worker.is_active
        )

        db_worker.turn_id = worker.turn_id if worker.turn_id else db_worker.turn_id

        db_worker.cost_center_id = (
            worker.cost_center_id if worker.cost_center_id else db_worker.cost_center_id
        )

        db_worker.department_id = (
            worker.department_id if worker.department_id else db_worker.department_id
        )

        db_worker.admission_date = (
            worker.admission_date if worker.admission_date else db_worker.admission_date
        )

        db_worker.resignation_date = (
            worker.resignation_date
            if worker.resignation_date
            else db_worker.resignation_date
        )

        session.add(db_worker)

        session.commit()

        session.refresh(db_worker)
    return db_worker


class WorkerDeactivateInput(BaseModel):
    is_active: bool
    resignation_date: str


@app.put("/workers/{id}/deactivate")
def deactivate_worker(id: int, worker: WorkerDeactivateInput):
    with Session(engine) as session:
        db_worker = session.get(Workers, id)

        db_worker.is_active = (
            worker.is_active if worker.is_active is not None else db_worker.is_active
        )

        db_worker.resignation_date = (
            worker.resignation_date
            if worker.resignation_date
            else db_worker.resignation_date
        )

        session.commit()

        session.refresh(db_worker)
    return db_worker


# functions


@app.get("/functions")
def get_functions():
    return handle_get_functions()


@app.get("/functions/for-users")
def get_functions_for_users():
    return handle_get_functions_for_users()


@app.get("/functions/for-workers")
def get_functions_for_users():
    return handle_get_functions_for_workers()


@app.post("/functions")
def post_function(function: Function):
    return handle_post_function(function)


@app.put("/functions/{id}")
def put_function(id: int, function: Function):
    return handle_put_function(id, function)


@app.delete("/functions/{id}")
def delete_function(id: int):
    return handle_delete_function(id)


# jobs


@app.get("/jobs")
def get_jobs():
    return handle_get_jobs()


@app.get("/jobs/subsidiarie/{subsidiarie_id}")
def get_jobs_by_subsidiarie_id(subsidiarie_id: int):
    return handle_get_jobs_by_subsidiarie_id(subsidiarie_id)


@app.post("/jobs")
def post_job(job: Jobs):
    return handle_post_job(job)


@app.delete("/jobs/{job_id}")
def delete_job(job_id: int):
    return handle_delete_job(job_id)


# roles


@app.get("/roles")
def get_roles():
    return handle_get_roles()


# candidates


@app.get("/candidates")
def get_candidates():
    return handle_get_candidates()


@app.get("/candidates/status/{id}")
def get_candidates_by_status(id: int):
    return handle_get_candidates_by_status(id)


@app.post("/candidates")
def post_candidate(candidate: Candidate):
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


@app.delete("/scales/{scale_id}/subsidiaries/{subsidiarie_id}")
def delete_scale(scale_id: int, subsidiarie_id: int):
    return handle_delete_scale(scale_id, subsidiarie_id)


# scale logs


@app.get("/logs/scales")
async def get_scales_logs():
    return await handle_database_operation(handle_get_scales_logs)


@app.post("/logs/scales")
async def post_scales_logs(scales_logs_input: ScaleLogs):
    return await handle_database_operation(handle_post_scale_logs, scales_logs_input)


# scale reports


@app.post("/reports/subsidiaries/{subsidiarie_id}/scales/days-on")
async def generate_scale_days_on_report(subsidiarie_id: int, input: ScalesReportInput):
    return await handle_database_operation(
        handle_generate_scale_days_on_report, subsidiarie_id, input
    )


@app.post("/reports/subsidiaries/{subsidiarie_id}/scales/days-off")
async def generate_scale_days_off_report(subsidiarie_id: int, input: ScalesReportInput):
    return await handle_database_operation(
        handle_generate_scale_days_off_report, subsidiarie_id, input
    )


# scrips


@app.post("/scripts/excel-scraping")
async def excel_scraping(file: UploadFile = File(...)):
    return await handle_excel_scraping(file)


# states


@app.get("/states")
async def get_states():
    return await handle_get_states()


@app.get("/states/{id}")
async def get_states_by_id(id: int):
    return await handle_get_states_by_id(id)


# cities


@app.get("/cities")
async def get_cities():
    return await handle_get_cities()


@app.get("/cities/{id}")
async def get_city_by_id(id: int):
    return await handle_get_city_by_id(id)


# cost center


@app.get("/cost-center")
async def get_cost_center():
    return await handle_database_operation(handle_get_cost_center)


@app.get("/cost-center/{id}")
async def get_cost_center_by_id(id: int):
    return await handle_database_operation(handle_get_cost_center_by_id, id)


@app.post("/cost-center")
async def post_cost_center(cost_center_input: CostCenter):
    return await handle_database_operation(handle_post_cost_center, cost_center_input)


@app.put("/cost-center/{id}")
async def put_cost_center(id: int, cost_center_input: CostCenter):
    return await handle_database_operation(
        handle_put_cost_center, id, cost_center_input
    )


@app.delete("/cost-center/{id}")
async def delete_cost_center(id: int):
    return await handle_database_operation(handle_delete_cost_center, id)


# department


@app.get("/departments")
async def get_departments():
    return await handle_database_operation(handle_get_departments)


@app.get("/departments/{id}")
async def get_department_by_id(id: int):
    return await handle_database_operation(handle_get_department_by_id, id)


@app.post("/departments")
async def post_department(department_input: Department):
    return await handle_database_operation(handle_post_department, department_input)


@app.put("/departments/{id}")
async def put_department(id: int, department_input: Department):
    return await handle_put_department(id, department_input)


@app.delete("/departments/{id}")
async def delete_department(id: int):
    return await handle_delete_department(id)
