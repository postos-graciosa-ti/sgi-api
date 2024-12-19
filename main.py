import calendar
import json
import os
import uuid
from datetime import date, datetime, timedelta
from typing import Any, List

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from passlib.hash import pbkdf2_sha256
from pydantic import BaseModel
from sqlmodel import Session, select, text

from controllers.candidato import (
    handle_delete_candidato,
    handle_get_candidato,
    handle_get_candidato_by_id,
    handle_post_candidato,
)
from controllers.functions import (
    handle_delete_function,
    handle_get_functions,
    handle_post_function,
    handle_put_function,
)
from controllers.months import handle_get_months
from controllers.scale import handle_delete_scale
from controllers.scales_controller import (
    handle_get_scales_history,
    handle_get_week_scale,
)
from controllers.subsidiaries import (
    handle_delete_subsidiarie,
    handle_get_subsidiaries,
    handle_post_subsidiaries,
    handle_put_subsidiarie,
)
from controllers.turn import (
    handle_delete_turn,
    handle_get_turns,
    handle_post_turns,
    handle_put_turns,
)
from controllers.users import (
    handle_delete_user,
    handle_get_users,
    handle_post_user,
    handle_put_user,
    handle_user_login,
)
from controllers.workers import (
    handle_get_active_workers_by_turn_and_subsidiarie,
    handle_get_workers_by_turn_and_subsidiarie,
)
from database.sqlite import create_db_and_tables, engine
from functions.scale import is_valid_scale
from middlewares.cors_middleware import add_cors_middleware
from models.candidate import Candidate
from models.candidate_status import CandidateStatus
from models.candidato import Candidato
from models.default_scale import DefaultScale
from models.function import Function
from models.jobs import Jobs
from models.month import Month
from models.role import Role
from models.scale import Scale
from models.scale_signature import ScaleSignature
from models.subsidiarie import Subsidiarie
from models.turn import Turn
from models.user import User
from models.user_subsidiaries import user_subsidiaries
from models.workers import Workers
from pyhints.scales import WeekScale
from seeds.seed_all import (
    seed_candidate_status,
    seed_database,
    seed_functions,
    seed_roles,
    seed_subsidiaries,
    seed_users,
)

load_dotenv()

app = FastAPI()

add_cors_middleware(app)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    seed_database()


# root


@app.get("/")
def docs():
    return {"docs": "acess /docs", "redocs": "access /redocs"}


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


@app.post("/users/login")
def user_login(user: User):
    return handle_user_login(user)


@app.get("/users")
def get_users():
    return handle_get_users()


@app.post("/users")
def post_user(user: User):
    return handle_post_user(user)


@app.put("/users/{id}")
def put_user(id: int, user: User):
    return handle_put_user(id, user)


@app.delete("/users/{id}")
def delete_user(id: int):
    return handle_delete_user(id)


# months


@app.get("/months")
def get_months():
    return handle_get_months()


# scale


@app.get("/scales/subsidiaries/{subsidiarie_id}")
def get_scales(subsidiarie_id: int):
    with Session(engine) as session:
        statement = select(Scale).where(Scale.subsidiarie_id == subsidiarie_id)

        scales = session.exec(statement).all()

        result = []

        for scale in scales:
            # Converte strings para listas usando `eval`, mas é melhor usar JSON (ajuste no modelo recomendado)
            workers_on = eval(scale.workers_on)

            workers_off = eval(scale.workers_off)

            # Obtem os detalhes dos trabalhadores de acordo com os IDs
            workers_on_data = [
                session.get(Workers, worker_on) for worker_on in workers_on
            ]

            workers_off_data = [
                session.get(Workers, worker_off) for worker_off in workers_off
            ]

            # Monta o dicionário para exibir os dados
            result.append(
                {
                    "scale_id": scale.id,
                    "date": scale.date,  # Certifique-se de que o modelo Scale tenha o campo `date`
                    "workers_on": [
                        {"id": worker.id, "name": worker.name}
                        for worker in workers_on_data
                        if worker
                    ],
                    "workers_off": [
                        {"id": worker.id, "name": worker.name}
                        for worker in workers_off_data
                        if worker
                    ],
                }
            )

        return result


class GetScalesByDate(BaseModel):
    initial_date: str
    end_date: str


@app.post("/scales/date")
def get_scales_by_date(formData: GetScalesByDate):
    initial = datetime.strptime(formData.initial_date, "%d/%m/%Y").date()

    end = datetime.strptime(formData.end_date, "%d/%m/%Y").date()

    with Session(engine) as session:
        statement = select(Scale).where(Scale.date >= initial, Scale.date <= end)
        scales = session.exec(statement).all()

        result = []

        for scale in scales:
            workers_on = eval(scale.workers_on)
            workers_off = eval(scale.workers_off)

            workers_on_data = [
                session.get(Workers, worker_on) for worker_on in workers_on
            ]

            workers_off_data = [
                session.get(Workers, worker_off) for worker_off in workers_off
            ]

            result.append(
                {
                    "scale_id": scale.id,
                    "date": scale.date,
                    "workers_on": [
                        {"id": worker.id, "name": worker.name}
                        for worker in workers_on_data
                        if worker
                    ],
                    "workers_off": [
                        {"id": worker.id, "name": worker.name}
                        for worker in workers_off_data
                        if worker
                    ],
                }
            )

        return result


@app.post("/scales")
def post_scale(formData: Scale):
    formData.date = datetime.strptime(formData.date, "%d/%m/%Y").date()

    with Session(engine) as session:
        session.add(formData)

        session.commit()

        session.refresh(formData)
    return formData


@app.delete("/scales/{id}")
def delete_scale(id: int):
    with Session(engine) as session:
        scale = session.get(Scale, id)

        session.delete(scale)

        session.commit()
    return {"message": "Escala deletada com sucesso"}


@app.get("/scale/signature/worker/{worker_id}/scale/{scale_id}")
def get_scale_signature(worker_id: int, scale_id: int):
    with Session(engine) as session:
        scale_signature = session.exec(
            select(ScaleSignature).where(
                ScaleSignature.worker_id == worker_id,
                ScaleSignature.scale_id == scale_id,
            )
        ).first()

        if scale_signature:
            return True
        else:
            return False


@app.post("/scale/signature")
def post_scale_signature(scale_signature: ScaleSignature):
    with Session(engine) as session:
        session.add(scale_signature)
        session.commit()
        session.refresh(scale_signature)
    return scale_signature


# @app.put("/scale/{id}")
# def put_scale(id: int, formData: Scale):
#     with Session(engine) as session:
#         scale = session.get(Scale, id)

#         scale.date = formData.date

#         scale.worker_id = formData.worker_id

#         scale.month_id = formData.month_id

#         session.add(scale)

#         session.commit()

#         session.refresh(scale)
#     return scale


# @app.delete("/scale/reset/worker/{worker_id}/month/{month_id}")
# def delete_scale(worker_id: int, month_id: int):
#     return handle_delete_scale(worker_id, month_id)


# subsidiaries


@app.get("/subsidiaries")
def get_subsidiaries():
    return handle_get_subsidiaries()


@app.post("/subsidiaries")
def post_subsidiaries(formData: Subsidiarie):
    return handle_post_subsidiaries(formData)


class PutSubsidiarie(BaseModel):
    name: str
    adress: str
    phone: str
    email: str


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


@app.post("/turns")
def post_turns(formData: Turn):
    return handle_post_turns(formData)


class PutTurn(BaseModel):
    name: str
    start_time: str
    start_interval_time: str
    end_time: str
    end_interval_time: str


@app.put("/turns/{id}")
def update_turn_schedule(id: int, formData: PutTurn):
    formData.start_time = datetime.strptime(formData.start_time, "%H:%M").time()

    formData.start_interval_time = datetime.strptime(
        formData.start_interval_time, "%H:%M"
    ).time()

    formData.end_time = datetime.strptime(formData.end_time, "%H:%M").time()

    formData.end_interval_time = datetime.strptime(
        formData.end_interval_time, "%H:%M"
    ).time()

    with Session(engine) as session:
        statement = select(Turn).where(Turn.id == id)

        turn = session.exec(statement).first()

        turn.name = formData.name

        turn.start_time = formData.start_time

        turn.start_interval_time = formData.start_interval_time

        turn.end_time = formData.end_time

        turn.end_interval_time = formData.end_interval_time

        session.commit()

        session.refresh(turn)
    return turn


@app.delete("/turns/{id}")
def delete_turn(id: int):
    return handle_delete_turn(id)


# workers


@app.get("/workers/turns/{turn_id}/subsidiarie/{subsidiarie_id}")
def get_workers_by_turn_and_subsidiarie(turn_id: int, subsidiarie_id: int):
    return handle_get_workers_by_turn_and_subsidiarie(turn_id, subsidiarie_id)


@app.get("/workers/on-track/turn/{turn_id}/subsidiarie/{subsidiarie_id}")
def get_active_workers_by_turn_and_subsidiarie(turn_id: int, subsidiarie_id: int):
    return handle_get_active_workers_by_turn_and_subsidiarie(turn_id, subsidiarie_id)


# xx


@app.post("/default_scale")
def create_default_scale(default_scale: DefaultScale):
    with Session(engine) as session:
        session.add(default_scale)
        session.commit()
        session.refresh(default_scale)
    return default_scale


@app.get("/default_scale")
def get_default_scale():
    with Session(engine) as session:
        default_scale = session.exec(select(DefaultScale)).all()
    return default_scale


@app.get("/workers/active/subsidiarie/{subsidiarie_id}/function/{function_id}")
def get_active_workers_by_subsidiarie_and_function(
    subsidiarie_id: int, function_id: int
):
    with Session(engine) as session:
        active_workers = session.exec(
            select(Workers).where(
                Workers.subsidiarie_id == subsidiarie_id,
                Workers.function_id == function_id,
                Workers.is_active == True,
            )
        ).all()
    return active_workers


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


# workers


@app.post("/workers")
def create_worker(worker: Workers):
    with Session(engine) as session:
        session.add(worker)
        session.commit()
        session.refresh(worker)
    return worker


@app.get("/workers/subsidiarie/{subsidiarie_id}")
def get_workers_by_subsidiarie(subsidiarie_id: int):
    with Session(engine) as session:
        workers = session.exec(
            select(Workers).where(Workers.subsidiarie_id == subsidiarie_id)
        ).all()
    return workers


@app.get("/jobs")
def get_jobs():
    with Session(engine) as session:
        jobs = session.exec(select(Jobs)).all()
    return jobs


@app.get("/jobs/subsidiarie/{subsidiarie_id}")
def get_jobs_by_subsidiarie(subsidiarie_id: int):
    with Session(engine) as session:
        jobs = session.exec(
            select(Jobs).where(Jobs.subsidiarie_id == subsidiarie_id)
        ).all()
    return jobs


@app.post("/jobs")
def create_job(job: Jobs):
    with Session(engine) as session:
        session.add(job)
        session.commit()
        session.refresh(job)
    return job


@app.delete("/jobs/{job_id}")
def delete_job(job_id: int):
    with Session(engine) as session:
        job = session.get(Jobs, job_id)

        if job:
            session.delete(job)
            session.commit()
    return {"message": "Job deleted successfully"}


@app.get("/roles")
def get_all_users():
    with Session(engine) as session:
        roles = session.exec(select(Role)).all()
    return roles


class GetUserRoles(BaseModel):
    id: int
    name: str
    email: str
    role: str


@app.get("/users_roles")
def get_users_roles():
    with Session(engine) as session:
        statement = select(
            User.id,
            User.name,
            User.email,
            Role.name,
        ).join(Role, User.role_id == Role.id, isouter=True)

        results = session.exec(statement)

        users = [
            GetUserRoles(
                id=result[0],
                name=result[1],
                email=result[2],
                role=result[3],
            )
            for result in results
        ]

        return users


@app.get("/users/{user_id}")
def get_user_by_id(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
    return user


class Test(BaseModel):
    arr: str


@app.post("/test")
def test(arr: Test):
    user_subsidiaries = eval(arr.arr)
    subsidiaries_array = []
    for subsidiary_id in user_subsidiaries:
        with Session(engine) as session:
            statement = select(Subsidiarie).where(Subsidiarie.id == subsidiary_id)
            subsidiary = session.exec(statement).first()
        subsidiaries_array.append(subsidiary)
    return subsidiaries_array


class VerifyEmail(BaseModel):
    email: str


@app.post("/verify-email")
def verify_email(userData: VerifyEmail):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == userData.email)).first()

    if user:
        return {"status": "true", "message": "Email existe no banco de dados."}
    else:
        return {"status": "false", "message": "Email não encontrado no banco de dados."}


class ConfirmPassword(BaseModel):
    email: str
    password: str


@app.post("/confirm-password")
def confirm_password(userData: ConfirmPassword):
    with Session(engine) as session:
        statement = select(User).where(User.email == userData.email)

        results = session.exec(statement)

        user = results.one()

        user.password = pbkdf2_sha256.hash(userData.password)

        # user.password = userData.password

        session.add(user)

        session.commit()

        session.refresh(user)

        return user


class PostCandidate(BaseModel):
    name: str
    date_of_birth: str
    adress: str
    resume: str
    job_id: int


@app.post("/candidates")
def post_candidate(candidate: Candidate):
    with Session(engine) as session:
        new_candidate = Candidate(
            name=candidate.name,
            date_of_birth=candidate.date_of_birth,
            adress="candidate.adress",
            resume=candidate.resume,
            job_id=candidate.job_id,
            status=2,
        )
        session.add(new_candidate)
        session.commit()
        session.refresh(new_candidate)

    return new_candidate


class GetCandidatesByStatus(BaseModel):
    status: int


@app.get("/candidates/status/{id}")
def get_candidates_by_status(id: int):
    with Session(engine) as session:
        candidates = session.exec(select(Candidate).where(Candidate.status == id)).all()
    return candidates


def calculate_day_off(mes: int, ano: int):
    # Obter o número total de dias no mês
    dias_no_mes = (datetime(ano, mes % 12 + 1, 1) - timedelta(days=1)).day

    # Lista de todos os dias do mês
    dias_do_mes = [datetime(ano, mes, dia) for dia in range(1, dias_no_mes + 1)]

    # Identificar todos os domingos no mês
    domingos = [dia.day for dia in dias_do_mes if dia.weekday() == 6]

    # Contar as folgas regulares (a cada 6 dias)
    folgas_regulares = list(range(1, dias_no_mes + 1, 6))

    # Verificar se algum domingo já está incluído nas folgas regulares
    domingos_nao_incluidos = [
        domingo for domingo in domingos if domingo not in folgas_regulares
    ]

    # Total de folgas
    total_folgas = len(folgas_regulares) + len(domingos_nao_incluidos)

    return {
        "dias_no_mês": dias_no_mes,
        "folgas_regulares": folgas_regulares,
        "domingos": domingos,
        "domingos_não_incluidos": domingos_nao_incluidos,
        "total_de_folgas": total_folgas,
    }


class Timedata(BaseModel):
    month: int
    year: int


@app.post("/generate-day-off")
def generate_day_off(timedata: Timedata):
    result = calculate_day_off(timedata.month, timedata.year)
    return result


@app.get("/scale/{date}")
def get_scale(date: str):
    with Session(engine) as session:
        scale = session.exec(select(Scale).where(Scale.date == date)).first()
    return scale


# class CreateScale(BaseModel):
#     date: str
#     workers_ids: str
#     subsidiarie_id: int
#     days_of_week: str
#     sundays: str


# @app.post("/scale/validate")
# def create_scale(scale: CreateScale):
#     proihbited_days = ["2024-12-01", "2024-12-02"]

#     workers_ids = eval(scale.workers_ids)

#     for worker_id in workers_ids:
#         for day in proihbited_days:
#             with Session(engine) as session:
#                 existing_scale = session.exec(
#                     select(Scale).where(
#                         Scale.date == day, Scale.workers_ids.contains(str(worker_id))
#                     )
#                 ).first()
#                 if existing_scale:
#                     return {
#                         "error": f"O trabalhador {worker_id} já está escalado para o dia {day}."
#                     }
#     return {"success": "Nenhum trabalhador está escalado para os dias proibidos."}


class ValidateWeekdaysScale(BaseModel):
    date: str
    workers_ids: str
    subsidiarie_id: int
    days_of_week: str
    # sundays: str


class ValidateSundaysScale(BaseModel):
    date: str
    workers_ids: str
    subsidiarie_id: int
    # days_of_week: str
    sundays: str


@app.post("/scale/validate/weekdays")
def validate_weekdays(scale: ValidateWeekdaysScale):
    workers_ids = eval(scale.workers_ids)

    proihbited_weekdays = eval(scale.days_of_week)

    is_valid_weekdays = is_valid_scale(workers_ids, proihbited_weekdays)

    return is_valid_weekdays


@app.get("/candidates")
def get_candidates():
    with Session(engine) as session:
        candidates = session.exec(select(Candidate)).all()
    return candidates


@app.post("/scale/validate/sundays")
def validate_sundays(scale: ValidateSundaysScale):
    workers_ids = eval(scale.workers_ids)

    proihbited_sundays = eval(scale.sundays)

    is_valid_sundays = is_valid_scale(workers_ids, proihbited_sundays)

    return is_valid_sundays


def get_week_scale(date: str):
    data = datetime.strptime(date, "%Y-%m-%d")

    dia_da_semana = data.weekday()

    segunda_feira = data - timedelta(days=dia_da_semana)

    domingo = data + timedelta(days=6 - dia_da_semana)

    datas_da_semana = [segunda_feira + timedelta(days=i) for i in range(7)]

    return [data.strftime("%Y-%m-%d") for data in datas_da_semana]


# @app.get("/scales")
# def get_all_scales():
#     with Session(engine) as session:
#         scales = session.exec(select(Scale)).all()
#     return scales


@app.post("/scale")
def scale_create(scale: List[Scale]):
    with Session(engine) as session:
        session.add_all(scale)
        session.commit()
        for item in scale:
            session.refresh(item)
    return scale


# @app.post("/scale/create")
# def scale_create(scale: Scale):
#     workers_ids = [int(n) for n in scale.workers_ids.split(",")]


class WorkersInArray(BaseModel):
    arr: str


class PutWorkerSecurity(BaseModel):
    security_password: str


class ScaleAgreed(BaseModel):
    user_id: int
    security_password: str
    # scale_date: str


# @app.post("/scales/agreed")
# def agreed_scales(data: ScaleAgreed):
#     with Session(engine) as session:
#         user = session.exec(select(User).where)


@app.put("/workers/{id}/security-password")
def put_worker_security_password(id: int, workerData: PutWorkerSecurity):
    with Session(engine) as session:
        worker = session.exec(select(Workers).where(Workers.id == id))

        worker.security_password = pbkdf2_sha256.hash(workerData.security_password)

        # session.commit()

        # session.refresh(worker)
    return worker


class Validate(BaseModel):
    security_password: str


# @app.post("/workers/{id}/security-password/validate")
# def post_security_password(id: int, data: Validate):
#     with Session(engine) as session:
#         worker = session.exec(select(Workers).where(Workers.id == id))

#         # return worker

#         if pbkdf2_sha256.verify(worker.security_password, data.security_password):
#             return True
#         else:
#             return False


class Test(BaseModel):
    id: int
    date: str
    subsidiarie_id: int
    workers: List


@app.get("/scales/subsidiarie/{id}")
def get_scales_by_subsidiarie(id: int) -> Any:
    # with Session(engine) as session:
    #     scales = session.exec(select(Scale).where(Scale.subsidiarie_id == id)).all()

    #     for scale in scales:
    #         print(scale)

    #         print(json.loads(scale.workers))

    #         scale.workers = json.loads(scale.workers)

    #     return scales

    with Session(engine) as session:
        scales = session.exec(
            select(Scale).where(Scale.subsidiarie_id == id)
        ).fetchall()

        if not scales:
            raise HTTPException(
                status_code=404, detail="No scales found for the given subsidiary ID."
            )

        for scale in scales:
            try:
                scale.workers = json.loads(scale.workers)
            except json.JSONDecodeError:
                raise HTTPException(
                    status_code=500, detail="Invalid JSON in 'workers' field."
                )

        return scales


@app.get("/workers")
def get_workers():
    with Session(engine) as session:
        workers = session.exec(select(Workers)).all()
    return workers


@app.post("/workers-in-array")
def workers_in_array(arr: WorkersInArray):
    user_subsidiaries = eval(arr.arr)

    subsidiaries_array = []

    for subsidiary_id in user_subsidiaries:
        with Session(engine) as session:
            statement = select(Workers).where(Workers.id == subsidiary_id)
            subsidiary = session.exec(statement).first()
        subsidiaries_array.append(subsidiary)
    return subsidiaries_array


class PutWorker(BaseModel):
    name: str
    function_id: int
    subsidiarie_id: int
    is_active: bool
    turn_id: int


@app.put("/workers/{worker_id}")
def update_worker(worker_id: int, worker_data: PutWorker):
    with Session(engine) as session:
        worker = session.exec(select(Workers).where(Workers.id == worker_id))
        worker.name = worker_data.name
        worker.function_id = worker_data.function_id
        worker.subsidiarie_id = worker_data.subsidiarie_id
        worker.turn_id = worker_data.turn_id


@app.post("/scales/{id}")
def scales_sla(id: int):
    with Session(engine) as session:
        scale = session.exec(select(Scale).where(Scale.id == id)).first()

        if not scale:
            raise HTTPException(status_code=404, detail="Scale not found")

        scale.agreed = True

        session.add(scale)

        session.commit()

        session.refresh(scale)

        selected_scale = session.exec(select(Scale).where(Scale.id == id)).first()

        return selected_scale


@app.put("/workers/deactivate/{worker_id}")
def deactivate_worker(worker_id: int):
    with Session(engine) as session:
        worker = session.get(Workers, worker_id)
        if worker:
            worker.is_active = False
            session.commit()
            session.refresh(worker)
            new_job = session.get(Function, worker.function_id)
            job = Jobs(
                name=new_job.name,
                description=new_job.description,
                subsidiarie_id=worker.subsidiarie_id,
            )
            session.add(job)
            session.commit()
            session.refresh(job)
            return job


@app.delete("/scales/{date}/{worker_id}")
def delete_scale(date: str, worker_id: int):
    with Session(engine) as session:
        scale = session.exec(
            select(Scale).where(
                Scale.workers_ids.contains(str(worker_id)),
                Scale.date == date,
            )
        ).first()
        if scale:
            session.delete(scale)
            session.commit()
            return {"message": "Escala deletada com sucesso"}
        else:
            return {"message": "Escala não encontrada"}


@app.put("/scales/{id}")
def put_scales(id: int, rows: list):
    for row in rows:
        with Session(engine) as session:
            db_row = session.exec(select(Scale).where(Scale.id == row.scale_id)).first()

            if db_row:
                db_row_workers = json.loads(db_row.workers)

                for worker in db_row_workers:
                    worker.status = row.status

                print(db_row)
            else:
                print(f"Scale with id {row.scale_id} not found.")


class Shift(BaseModel):
    scale_id: int
    worker_id: int
    status: str


@app.post("/shifts/")
def create_shifts(shifts: List[Shift]):
    for shift in shifts:
        print(f"Processing shift: {shift}")

        with Session(engine) as session:
            db_row = session.exec(
                select(Scale).where(Scale.id == shift.scale_id)
            ).first()

            if db_row:
                print(f"Found scale: {db_row}")

                workers = json.loads(db_row.workers)

                print(f"Workers before update: {workers}")

                for worker in workers:
                    if worker["id"] == shift.worker_id:
                        worker["status"] = shift.status
                        print(f"Updated worker: {worker}")

                db_row.workers = json.dumps(workers)

                session.add(db_row)

                session.commit()

                print(f"Updated workers saved in database: {workers}")

    return {"message": "Shifts updated successfully"}
