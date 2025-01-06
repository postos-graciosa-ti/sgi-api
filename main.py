from aiocache import Cache, cached
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
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
    handle_get_scales_by_subsidiarie_and_worker_id,
    handle_get_scales_by_subsidiarie_id,
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
    with Session(engine) as session:
        subsidiarie = session.exec(
            select(Subsidiarie).where(Subsidiarie.id == id)
        ).one()

        return subsidiarie


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
        statement = (
            select(
                Candidate.id,
                Candidate.name,
                Candidate.date_of_birth,
                Candidate.adress,
                Candidate.resume,
                Candidate.status,
                Jobs.id.label("job_id"),
                Jobs.name.label("job_name"),
            )
            .join(Jobs, Candidate.job_id == Jobs.id)
            .where(Candidate.status == id)
        )

        candidates = session.exec(statement).all()

        return JSONResponse(
            [
                {
                    "candidate_id": candidate[0],
                    "name": candidate[1],
                    "date_of_birth": candidate[2],
                    "adress": candidate[3],
                    "resume": candidate[4],
                    "status": candidate[5],
                    "job_id": candidate[6],
                    "job_name": candidate[7],
                }
                for candidate in candidates
            ]
        )


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
    return handle_get_scales_by_subsidiarie_id(subsidiarie_id)


@app.get("/scales/subsidiaries/{subsidiarie_id}/workers/{worker_id}")
def get_scales_by_subsidiarie_and_worker_id(subsidiarie_id: int, worker_id: int):
    return handle_get_scales_by_subsidiarie_and_worker_id(subsidiarie_id, worker_id)


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


class GetStatesOutput(BaseModel):
    label: str
    value: int


@app.get("/states")
@cached(ttl=3600, cache=Cache.MEMORY)
async def get_states():
    with Session(engine) as session:
        states = session.exec(select(States)).all()

        return [GetStatesOutput(label=state.name, value=state.id) for state in states]


@app.get("/states/{id}")
def get_states_by_id(id: int):
    with Session(engine) as session:
        state = session.exec(select(States).where(States.id == id)).all()

        return state


# cities


class GetCitiesOutput(BaseModel):
    label: str
    value: int


@app.get("/cities")
@cached(ttl=3600, cache=Cache.MEMORY)
async def get_cities():
    with Session(engine) as session:
        cities = session.exec(select(Cities)).all()

        return [GetCitiesOutput(label=city.name, value=city.id) for city in cities]


@app.get("/cities/{id}")
def get_city_by_id(id: int):
    with Session(engine) as session:
        city = session.exec(select(Cities).where(Cities.id == id)).one()

        return city
