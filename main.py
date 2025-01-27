import json
from datetime import datetime, timedelta

import cloudinary
import cloudinary.uploader
from aiocache import Cache, cached
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, or_, select

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
)
from controllers.scales_logs import handle_get_scales_logs
from controllers.subsidiaries import (
    handle_delete_subsidiarie,
    handle_get_subsidiarie_by_id,
    handle_get_subsidiaries,
    handle_post_subsidiaries,
    handle_put_subsidiarie,
)
from controllers.turn import (
    handle_delete_turn,
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
    handle_get_workers_by_subsidiarie,
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
from models.cities import Cities
from models.cost_center import CostCenter
from models.department import Department
from models.function import Function
from models.jobs import Jobs
from models.scale import Scale
from models.scale_logs import ScaleLogs
from models.states import States
from models.subsidiarie import Subsidiarie
from models.turn import Turn
from models.user import User
from models.workers import Workers
from pyhints.scales import PostScaleInput
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

cache = Cache(Cache.MEMORY, ttl=3600)

cloudinary.config(
    cloud_name="drvzslkwn",
    api_key="526373414174189",
    api_secret="9NsMrkZPADrJIbSzd1JgfAKQnyI",
    secure=True,
)

# root


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

    seed_database()


@app.get("/")
def get_docs_info():
    return handle_get_docs_info()


@app.get("/render-server/activate")
def activate_render_server():
    return handle_activate_render_server()


@app.post("/upload")
async def upload_file(
    name: str = Form(...),
    date_of_birth: str = Form(...),
    adress: str = Form(...),
    resume: UploadFile = File(...),
    status: int = Form(...),
    job_id: int = Form(...),
):
    date_of_birth = datetime.strptime(date_of_birth, "%d-%m-%Y")

    file_content = await resume.read()

    upload_result = cloudinary.uploader.upload(
        file_content, resource_type="raw", public_id=resume.filename
    )

    candidate = Candidate(
        name=name,
        date_of_birth=date_of_birth.strftime("%d-%m-%Y"),
        adress=adress,
        resume=upload_result["secure_url"],
        status=status,
        job_id=job_id,
    )

    with Session(engine) as session:
        session.add(candidate)

        session.commit()

        session.refresh(candidate)

    return candidate


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


# turn


@app.get("/turns")
def get_turns():
    return handle_get_turns()


@app.get("/turns/{id}")
def handle_get_turn_by_id(id: int):
    with Session(engine) as session:
        turn = session.exec(select(Turn).where(Turn.id == id)).one()

        return turn


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
def get_worker_by_id(id: int):
    with Session(engine) as session:
        worker = session.exec(select(Workers).where(Workers.id == id)).one()

        return worker


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


@app.post("/workers")
def post_worker(worker: Workers):
    return handle_post_worker(worker)


@app.put("/workers/{id}")
def put_worker(id: int, worker: Workers):
    return handle_put_worker(id, worker)


@app.put("/workers/deactivate/{worker_id}")
def deactivate_worker(worker_id: int):
    return handle_deactivate_worker(worker_id)


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


@app.delete("/scales/{scale_id}/subsidiaries/{subsidiarie_id}")
def delete_scale(scale_id: int, subsidiarie_id: int):
    return handle_delete_scale(scale_id, subsidiarie_id)


# scrips


@app.post("/scripts/excel-scraping")
async def excel_scraping(file: UploadFile = File(...)):
    return await handle_excel_scraping(file)


# states


@app.get("/states")
@cached(ttl=3600, cache=Cache.MEMORY)
async def get_states():
    return await handle_get_states()


@app.get("/states/{id}")
async def get_states_by_id(id: int):
    return await handle_get_states_by_id(id)


# cities


@app.get("/cities")
@cached(ttl=3600, cache=Cache.MEMORY)
async def get_cities():
    return await handle_get_cities()


@app.get("/cities/{id}")
async def get_city_by_id(id: int):
    return await handle_get_city_by_id(id)


class ScalesReportInput(BaseModel):
    initial_date: str
    final_date: str


@app.post("/subsidiaries/{id}/scales/report")
def get_scales_report(id: int, scale_report_input: ScalesReportInput):
    # graciosa matriz report
    if id == 1:
        with Session(engine) as session:
            first_day_date = datetime.strptime(
                scale_report_input.initial_date, "%d-%m-%Y"
            )
            last_day_date = datetime.strptime(scale_report_input.final_date, "%d-%m-%Y")

            dias_do_mes = []
            data_atual = first_day_date

            while data_atual <= last_day_date:
                dias_do_mes.append(data_atual.strftime("%d-%m-%Y"))
                data_atual += timedelta(days=1)

            def generate_turn_report(turn_id):
                turn_info = session.get(Turn, turn_id)
                turn_report = [{"turn_info": turn_info}]

                for dia_do_mes in dias_do_mes:
                    frentistas_ao_dia = session.exec(
                        select(Scale)
                        .where(Scale.days_on.contains(dia_do_mes))
                        .where(Scale.worker_turn_id == turn_id)
                        .where(
                            or_(
                                Scale.worker_function_id == 4,
                                Scale.worker_function_id == 2,
                            )
                        )
                    ).all()

                    nomes_frentistas_ao_dia = [
                        session.get(Workers, frentista.worker_id)
                        for frentista in frentistas_ao_dia
                    ]

                    trocadores_ao_dia = session.exec(
                        select(Scale)
                        .where(Scale.days_on.contains(dia_do_mes))
                        .where(Scale.worker_turn_id == turn_id)
                        .where(Scale.worker_function_id == 9)
                    ).all()

                    nomes_trocadores_ao_dia = [
                        session.get(Workers, trocador.worker_id)
                        for trocador in trocadores_ao_dia
                    ]

                    turn_report.append(
                        {
                            "date": dia_do_mes,
                            "nomes_frentistas": nomes_frentistas_ao_dia,
                            "quantidade_frentistas": len(frentistas_ao_dia),
                            "nomes_trocadores": nomes_trocadores_ao_dia,
                            "quantidade_trocadores": len(trocadores_ao_dia),
                            "status": (
                                "trabalhadores suficientes"
                                if len(trocadores_ao_dia) >= 1
                                and len(frentistas_ao_dia) >= 3
                                else "trabalhadores insuficientes"
                            ),
                        }
                    )
                return turn_report

            report = {
                "primeiro_turno_report": generate_turn_report(2),
                "segundo_turno_report": generate_turn_report(1),
                "terceiro_turno_report": generate_turn_report(3),
                "quarto_turno_report": generate_turn_report(4),
                "quinto_turno_report": generate_turn_report(5),
                "sexto_turno_report": generate_turn_report(6),
            }

            return report


class PrintScaleInput(BaseModel):
    initial_date: str
    end_date: str


@app.post("/subsidiaries/{subsidiarie_id}/prints/{print_id}/scales")
def print_scales(
    subsidiarie_id: int, print_id: int, print_scales_input: PrintScaleInput
):
    if print_id == 1:
        with Session(engine) as session:
            primeiro_turno_info = session.get(Turn, 2)

            segundo_turno_info = session.get(Turn, 1)

            terceiro_turno_info = session.get(Turn, 3)

            first_day_date = datetime.strptime(
                print_scales_input.initial_date, "%d-%m-%Y"
            )

            last_day_date = datetime.strptime(print_scales_input.end_date, "%d-%m-%Y")

            dias_do_mes = []
            data_atual = first_day_date

            while data_atual <= last_day_date:
                dias_do_mes.append(data_atual.strftime("%d-%m-%Y"))
                data_atual += timedelta(days=1)

            def get_folgas(turno_id, turno_info):
                folgas = [
                    {
                        "turn_info": {
                            "start_time": turno_info.start_time,
                            "end_time": turno_info.end_time,
                        }
                    }
                ]

                for dia_do_mes in dias_do_mes:
                    frentistas_de_folga = session.exec(
                        select(Workers)
                        .join(Scale, Scale.worker_id == Workers.id)
                        .where(Scale.subsidiarie_id == subsidiarie_id)
                        .where(Scale.days_off.contains(dia_do_mes))
                        .where(Scale.worker_turn_id == turno_id)
                        .where(Scale.worker_function_id == 6)
                    ).all()

                    trocadores_de_folga = session.exec(
                        select(Workers)
                        .join(Scale, Scale.worker_id == Workers.id)
                        .where(Scale.subsidiarie_id == subsidiarie_id)
                        .where(Scale.days_off.contains(dia_do_mes))
                        .where(Scale.worker_turn_id == turno_id)
                        .where(Scale.worker_function_id == 8)
                    ).all()

                    frentistas_turno = [worker for worker in frentistas_de_folga]
                    trocadores_turno = [worker for worker in trocadores_de_folga]

                    folgas.append(
                        {
                            "date": dia_do_mes,
                            "frentistas": frentistas_turno,
                            "trocadores": trocadores_turno,
                        }
                    )

                return folgas

            primeiro_turno_folgas = get_folgas(1, primeiro_turno_info)
            segundo_turno_folgas = get_folgas(2, segundo_turno_info)
            terceiro_turno_folgas = get_folgas(3, terceiro_turno_info)

            return {
                "primeiro_turno_folgas": primeiro_turno_folgas,
                "segundo_turno_folgas": segundo_turno_folgas,
                "terceiro_turno_folgas": terceiro_turno_folgas,
            }
    else:
        return {"nothing": "nothing"}


@app.get("/logs/scales")
async def get_scales_logs():
    return await handle_database_operation(handle_get_scales_logs)


@app.post("/logs/scales")
def post_scales_logs(scales_logs_input: ScaleLogs):
    with Session(engine) as session:
        session.add(scales_logs_input)

        session.commit()

        session.refresh(scales_logs_input)
    return scales_logs_input


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
