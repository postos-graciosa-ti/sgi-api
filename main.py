import json
from datetime import datetime, timedelta

import cloudinary
import cloudinary.uploader
from aiocache import Cache, cached
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select

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
from controllers.functions import (
    handle_delete_function,
    handle_get_functions,
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
    handle_get_scales_by_subsidiarie_and_worker_id,
    handle_get_scales_by_subsidiarie_id,
    handle_post_scale,
)
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
from middlewares.cors_middleware import add_cors_middleware
from models.candidate import Candidate
from models.candidato import Candidato
from models.cities import Cities
from models.function import Function
from models.jobs import Jobs
from models.scale import Scale
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


class Test(SQLModel, Table=True):
    id: int = Field(default=None, primary_key=True)
    station_attendant: str = Field(default="[]")
    operator: str = Field(default="[]")


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
    with Session(engine) as session:
        has_users = session.exec(select(User)).all()

        result = bool(has_users)

        return result


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


# class NeedAlertInput(BaseModel):
#     days_off: str
#     first_day: str
#     last_day: str


# @app.post("/scales/need-alert")
# def teste(form_data: NeedAlertInput):
#     form_data.days_off = eval(form_data.days_off)

#     first_day = datetime.strptime(form_data.first_day, "%d-%m-%Y")

#     last_day = datetime.strptime(form_data.last_day, "%d-%m-%Y")

#     dias_do_mes = []

#     data_atual = first_day

#     while data_atual <= last_day:
#         dias_do_mes.append(data_atual.strftime("%d-%m-%Y"))
#         data_atual += timedelta(days=1)

#     dias_sem_folga = [dia for dia in dias_do_mes if dia not in form_data.days_off]

#     all_dates = sorted(dias_sem_folga + form_data.days_off)

#     options = [
#         {"dayOff": date in form_data.days_off, "value": date} for date in all_dates
#     ]

#     dias_consecutivos = []
#     contador = 0
#     tem_mais_de_oito_dias_consecutivos = False

#     for dia in options:
#         if dia["dayOff"]:
#             dias_consecutivos.append({"dias": contador, "dataFolga": dia["value"]})
#             contador = 0
#         else:
#             contador += 1
#             if contador > 8:
#                 tem_mais_de_oito_dias_consecutivos = True

#     return tem_mais_de_oito_dias_consecutivos


# class TestingInput(BaseModel):
#     date_from_calendar: str
#     date_to_compare: str


# @app.post("/testing")
# def testing(form_data: TestingInput):
#     date_from_calendar = datetime.strptime(form_data.date_from_calendar, "%d-%m-%Y")

#     date_to_compare = datetime.strptime(form_data.date_to_compare, "%d-%m-%Y")

#     date_difference = date_to_compare - date_from_calendar

#     return {"date_difference": date_difference.days}


@app.post("/scales")
def post_scale(form_data: PostScaleInput):
    return handle_post_scale(form_data)


@app.delete("/scales/{scale_id}/subsidiaries/{subsidiarie_id}")
def delete_scale(scale_id: int, subsidiarie_id: int):
    return handle_delete_scale(scale_id, subsidiarie_id)


from pydantic import BaseModel


# Modelo para o corpo da requisição
class ValidateScaleRequest(BaseModel):
    first_day: str
    last_day: str


@app.post("/validate_monthly_scale/{subsidiarie_id}")
def validate_monthly_scale(subsidiarie_id: int, request: ValidateScaleRequest):
    try:
        first_day_date = datetime.strptime(request.first_day, "%d-%m-%Y")
        last_day_date = datetime.strptime(request.last_day, "%d-%m-%Y")

        # Gera os dias do mês
        dias_do_mes = []
        data_atual = first_day_date
        while data_atual <= last_day_date:
            dias_do_mes.append(data_atual.strftime("%d-%m-%Y"))
            data_atual += timedelta(days=1)

        validation_results = []

        with Session(engine) as session:
            for dia in dias_do_mes:
                # Obtém os trabalhadores escalados para o dia
                workers_on_day = session.exec(
                    select(Workers)
                    .join(Scale, Workers.id == Scale.worker_id)
                    .where(
                        Scale.subsidiarie_id == subsidiarie_id,
                        Scale.days_on.contains(f'"{dia}"'),
                    )
                ).all()

                # Conta os trabalhadores por função
                frentistas = sum(
                    1 for worker in workers_on_day if worker.function_id == 6
                )
                trocadores = sum(
                    1 for worker in workers_on_day if worker.function_id == 8
                )

                if frentistas < 3 or trocadores < 1:
                    validation_results.append(
                        {
                            "date": dia,
                            "frentistas": frentistas,
                            "trocadores": trocadores,
                            "status": "Insufficient workers",
                        }
                    )
                else:
                    validation_results.append(
                        {
                            "date": dia,
                            "frentistas": frentistas,
                            "trocadores": trocadores,
                            "status": "Sufficient workers",
                        }
                    )

        return {"validation_results": validation_results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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


@app.get("/subsidiaries/{id}/frentistas")
def get_frentistas(id: int):
    with Session(engine) as session:
        frentistas = session.exec(
            select(Workers)
            .where(Workers.function_id == 6)
            .where(Workers.subsidiarie_id == id)
        ).all()

        return frentistas


@app.get("/subsidiaries/{id}/caixas")
def get_caixas(id: int):
    with Session(engine) as session:
        caixas = session.exec(
            select(Workers)
            .where(Workers.function_id == 7)
            .where(Workers.subsidiarie_id == id)
        ).all()

        return caixas


@app.get("/subsidiaries/{id}/trocadores-de-oleo")
def get_trocadores_de_oleo(id: int):
    with Session(engine) as session:
        trocadores_de_oleo = session.exec(
            select(Workers)
            .where(Workers.function_id == 8)
            .where(Workers.subsidiarie_id == id)
        ).all()

        return trocadores_de_oleo


class SlaScale(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    date: str = Field(index=True)
    weekday: str = Field(index=True)
    subsidiarie_id: int = Field(default=None, foreign_key="subsidiarie.id")
    turn_id: int = Field(default=None, foreign_key="turn.id")
    workers_on_ids: str = Field(default="[]")
    workers_off_ids: str = Field(default="[]")


@app.get("/subsidiaries/{id}/sla-scale")
def get_sla_scale(id: int):
    with Session(engine) as session:
        scales = session.exec(
            select(
                SlaScale.id,
                SlaScale.date,
                SlaScale.weekday,
                SlaScale.subsidiarie_id,
                SlaScale.turn_id,
                SlaScale.workers_on_ids,
                SlaScale.workers_off_ids,
                Turn.id.label("turn_id"),
                Turn.start_time.label("turn_start_time"),
                Turn.end_time.label("turn_end_time"),
            )
            .join(Turn, Turn.id == SlaScale.turn_id)
            .where(SlaScale.subsidiarie_id == id)
        ).all()

        result = []

        for scale in scales:
            workers_on_ids = json.loads(scale.workers_on_ids)

            workers_off_ids = json.loads(scale.workers_off_ids)

            workers_on = [
                session.get(Workers, worker_on_id) for worker_on_id in workers_on_ids
            ]

            workers_off = [
                session.get(Workers, worker_off_id) for worker_off_id in workers_off_ids
            ]

            result.append(
                {
                    "sla_scale_id": scale.id,
                    "date": scale.date,
                    "weekday": scale.weekday,
                    "workers_on": [worker for worker in workers_on if worker],
                    "workers_off": [worker for worker in workers_off if worker],
                    "turn_id": scale.turn_id,
                    "turn_start_time": scale.turn_start_time,
                    "turn_end_time": scale.turn_end_time,
                }
            )

        return result


@app.post("/sla-scale")
def post_sla_scale(scale: SlaScale):
    with Session(engine) as session:
        session.add(scale)

        session.commit()

        session.refresh(scale)
    return scale


# ~~


@app.post("/scale")
def post_scale(scale: Test):
    with Session(engine) as session:
        session.add(scale)

        session.commit()

        session.refresh(scale)
    return scale
