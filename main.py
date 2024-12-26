import calendar
import json
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from controllers.candidato import (
    handle_delete_candidato,
    handle_get_candidato,
    handle_get_candidato_by_id,
    handle_post_candidato,
)
from controllers.docs import handle_get_docs_info
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
from controllers.scale import (
    handle_delete_scale,
    handle_get_scale_by_date,
    handle_get_scale_by_subsidiarie_id,
    handle_post_scale,
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
    handle_put_turn,
)
from controllers.users import (
    handle_confirm_password,
    handle_delete_user,
    handle_get_test,
    handle_get_user_by_id,
    handle_get_users,
    handle_get_users_roles,
    handle_post_user,
    handle_put_user,
    handle_user_login,
    handle_verify_email,
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
from middlewares.cors_middleware import add_cors_middleware
from models.candidate import Candidate
from models.candidato import Candidato
from models.function import Function
from models.jobs import Jobs
from models.scale import Scale
from models.subsidiarie import Subsidiarie
from models.turn import Turn
from models.user import User
from models.workers import Workers
from pyhints.scales import GetScalesByDate
from pyhints.subsidiaries import PutSubsidiarie
from pyhints.turns import PutTurn
from pyhints.users import ConfirmPassword, Test, VerifyEmail
from seeds.seed_all import seed_database

# pre settings

load_dotenv()

app = FastAPI()

add_cors_middleware(app)

# root


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

    seed_database()


@app.get("/")
def docs_info():
    return handle_get_docs_info()


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
def get_users():
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


@app.post("/verify-email")
def verify_email(userData: VerifyEmail):
    return handle_verify_email(userData)


@app.post("/confirm-password")
def confirm_password(userData: ConfirmPassword):
    return handle_confirm_password(userData)


# months


@app.get("/months")
def get_months():
    return handle_get_months()


# scale


# @app.get("/scales/subsidiaries/{subsidiarie_id}")
# def get_scales(subsidiarie_id: int):
#     return handle_get_scale_by_subsidiarie_id(subsidiarie_id)


# @app.post("/scales/date")
# def get_scales_by_date(formData: GetScalesByDate):
#     return handle_get_scale_by_date(formData)


# @app.post("/scales")
# def post_scale(formData: Scale):
#     return handle_post_scale(formData)


# @app.delete("/scales/{id}")
# def delete_scale(id: int):
#     return handle_delete_scale(id)


# subsidiaries


@app.get("/subsidiaries")
def get_subsidiaries():
    return handle_get_subsidiaries()


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
    with Session(engine) as session:
        candidates = session.exec(select(Candidate)).all()
    return candidates


@app.get("/candidates/status/{id}")
def get_candidates_by_status(id: int):
    with Session(engine) as session:
        candidates = session.exec(select(Candidate).where(Candidate.status == id)).all()
    return candidates


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


# scales


@app.get("/scales/subsidiaries/{subsidiarie_id}")
def get_scales_by_subsidiarie_id(subsidiarie_id: int):
    with Session(engine) as session:
        statement = select(Scale).where(Scale.subsidiarie_id == subsidiarie_id)

        scales_by_subsidiarie = session.exec(statement).all()

        format_scales = []

        for scale in scales_by_subsidiarie:
            format_scale = {
                "id": scale.id,
                # 'worker_id': scale.worker_id,
                "worker": session.get(Workers, scale.worker_id),
                "days_on": eval(scale.days_on),
                "days_off": eval(scale.days_off),
                "need_alert": scale.need_alert,
                "proportion": scale.proportion,
            }

            format_scales.append(format_scale)

    return format_scales


@app.get("/scales/subsidiaries/{subsidiarie_id}/workers/{worker_id}")
def get_scales_by_subsidiarie_and_worker_id(subsidiarie_id: int, worker_id: int):
    with Session(engine) as session:
        statement = (
            select(Scale)
            .where(Scale.subsidiarie_id == subsidiarie_id)
            .where(Scale.worker_id == worker_id)
        )

        scales_by_subsidiarie_and_worker_id = session.exec(statement).first()

        return eval(scales_by_subsidiarie_and_worker_id.days_off)


class FormData(BaseModel):
    worker_id: int
    subsidiarie_id: int
    days_off: str
    first_day: str
    last_day: str


@app.post("/scales")
async def save_or_update_days_off(form_data: FormData):
    try:
        form_data.days_off = eval(form_data.days_off)

        first_day = datetime.strptime(form_data.first_day, "%d-%m-%Y")
        
        last_day = datetime.strptime(form_data.last_day, "%d-%m-%Y")
        
        dias_do_mes = []
        
        data_atual = first_day
        
        while data_atual <= last_day:
            dias_do_mes.append(data_atual.strftime("%d-%m-%Y"))
            data_atual += timedelta(days=1)
        
        # Dias sem folga
        dias_sem_folga = [
            dia for dia in dias_do_mes if dia not in form_data.days_off
        ]
        
        # Calcula proporção e verifica se há mais de 8 dias consecutivos sem folga
        all_dates = sorted(dias_sem_folga + form_data.days_off)
        options = [
            {"dayOff": date in form_data.days_off, "value": date}
            for date in all_dates
        ]

        dias_consecutivos = []
        contador = 0
        tem_mais_de_oito_dias_consecutivos = False

        for dia in options:
            if dia["dayOff"]:
                dias_consecutivos.append({
                    "dias": contador,
                    "dataFolga": dia["value"]
                })
                contador = 0
            else:
                contador += 1
                if contador > 8:
                    tem_mais_de_oito_dias_consecutivos = True

        proporcoes = [
            {
                "folga": idx + 1,
                "data": item["dataFolga"],
                "proporcao": f"{item['dias']}x1"
            }
            for idx, item in enumerate(dias_consecutivos)
        ]

        # Verificação de erro se não houver dias de folga
        if not form_data.days_off:
            raise HTTPException(status_code=400, detail="Não é possível salvar sem dias de folga.")

        # Gerenciamento da sessão com contexto `with`
        with Session(engine) as session:
            # Verifica se já existe um registro com o mesmo worker_id e subsidiarie_id
            existing_scale = session.exec(
                select(Scale).where(
                    Scale.worker_id == form_data.worker_id,
                    Scale.subsidiarie_id == form_data.subsidiarie_id
                )
            ).first()

            if existing_scale:
                # Atualiza os dados do registro existente
                existing_scale.days_on = json.dumps(dias_sem_folga)
                existing_scale.days_off = json.dumps(form_data.days_off)
                existing_scale.need_alert = tem_mais_de_oito_dias_consecutivos
                existing_scale.proportion = json.dumps(proporcoes)
            else:
                # Cria um novo registro
                existing_scale = Scale(
                    worker_id=form_data.worker_id,
                    subsidiarie_id=form_data.subsidiarie_id,
                    days_on=json.dumps(dias_sem_folga),
                    days_off=json.dumps(form_data.days_off),
                    need_alert=tem_mais_de_oito_dias_consecutivos,
                    proportion=json.dumps(proporcoes)
                )
                session.add(existing_scale)

            # Salva as mudanças no banco
            session.commit()
            session.refresh(existing_scale)

        # Retorna os dados atualizados ou inseridos
        return eval(existing_scale.days_off)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




# @app.post("/scales")
# def post_scale(scale: Scale):
#     with Session(engine) as session:
#         statement = select(Scale).where(Scale.worker_id == scale.worker_id)

#         scales_by_worker_id = session.exec(statement).first()

#         if scales_by_worker_id:
#             current_days_off = eval(scales_by_worker_id.days_off)

#             new_days_off = eval(scale.days_off)

#             merged_days_off = list(set(current_days_off + new_days_off))

#             merged_days_off.sort()

#             scales_by_worker_id.days_off = str(merged_days_off)

#             days_on = eval(scale.days_on)

#             days_on.sort()

#             scales_by_worker_id.days_on = str(days_on)

#             scales_by_worker_id.need_alert = scale.need_alert

#             scales_by_worker_id.proportion = scale.proportion

#             session.commit()

#             session.refresh(scales_by_worker_id)

#             return eval(scales_by_worker_id.days_off)
#         else:
#             session.add(scale)

#             session.commit()

#             session.refresh(scale)

#             return eval(scale.days_off)


class Date(BaseModel):
    date: str


@app.post("/scales/workers/{worker_id}")
def get_scales_by_worker_id(worker_id: int, formData: Date):
    with Session(engine) as session:
        worker_scale = session.exec(
            select(Scale).where(Scale.worker_id == worker_id)
        ).first()

        worker_scale_dates_off = eval(worker_scale.days_off)

        worker_scale_dates_on = eval(worker_scale.days_on)

        if formData.date in worker_scale_dates_off:
            worker_scale_dates_off.remove(formData.date)

            worker_scale_dates_on.append(formData.date)

        worker_scale_dates_off.sort()

        worker_scale_dates_on.sort()

        worker_scale_dates_off.sort()

        worker_scale.days_off = str(worker_scale_dates_off)

        worker_scale_dates_on.sort()

        worker_scale.days_on = str(worker_scale_dates_on)

        worker_scale_proportion = json.loads(worker_scale.proportion)

        updated_proportion = [
            proportion
            for proportion in worker_scale_proportion
            if proportion["data"] != formData.date
        ]

        worker_scale.proportion = json.dumps(updated_proportion)

        session.commit()

        session.refresh(worker_scale)

        return {"days_off": worker_scale_dates_off, "days_on": worker_scale_dates_on}


@app.delete("/scales/{scale_id}/subsidiaries/{subsidiarie_id}")
def delete_scale(scale_id: int, subsidiarie_id: int):
    with Session(engine) as session:
        session.delete(session.get(Scale, scale_id))

        session.commit()

        statement = select(Scale).where(Scale.subsidiarie_id == subsidiarie_id)

        all_scales_by_subsidiarie = session.exec(statement).all()

    return all_scales_by_subsidiarie
