from datetime import date

from sqlmodel import Session, select, update

from database.sqlite import engine
from models.function import Function
from models.jobs import Jobs
from models.scale import Scale
from models.turn import Turn
from models.workers import Workers


def handle_get_workers_by_subsidiarie(subsidiarie_id: int):
    with Session(engine) as session:
        workers = session.exec(
            select(
                Workers.id,
                Workers.name,
                Workers.is_active,
                Function.id.label("function_id"),
                Function.name.label("function_name"),
                Turn.id.label("turn_id"),
                Turn.name.label("turn_name"),
                Turn.start_time.label("turn_start_time"),
                Turn.end_time.label("turn_end_time")
            )
            .where(Workers.subsidiarie_id == subsidiarie_id)
            .join(Function, Function.id == Workers.function_id)
            .join(Turn, Workers.turn_id == Turn.id)
        ).all()

        return [
            {
                "worker_id": worker.id,
                "worker_name": worker.name,
                "worker_is_active": worker.is_active,
                "function_id": worker.function_id,
                "function_name": worker.function_name,
                "turn_id": worker.turn_id,
                "turn_name": worker.turn_name,
                "turn_start_time": worker.turn_start_time,
                "turn_end_time": worker.turn_end_time
            }
            for worker in workers
        ]


def handle_put_worker(id: int, worker: Workers):
    with Session(engine) as session:
        db_worker = session.get(Workers, id)

        if db_worker:
            db_worker.name = worker.name

            db_worker.function_id = worker.function_id

            db_worker.subsidiarie_id = worker.subsidiarie_id

            db_worker.turn_id = worker.turn_id

            db_worker.is_active = worker.is_active

            session.add(db_worker)

            session.commit()

            session.refresh(db_worker)

            return db_worker
        else:
            return {"error": "Worker not found"}


def handle_get_workers_by_turn_and_subsidiarie(turn_id: int, subsidiarie_id: int):
    with Session(engine) as session:
        statement = select(Workers).where(
            Workers.turn_id == turn_id, Workers.subsidiarie_id == subsidiarie_id
        )

        workers = session.exec(statement).all()

    return workers


def handle_get_active_workers_by_turn_and_subsidiarie(
    turn_id: int, subsidiarie_id: int
):
    with Session(engine) as session:
        statement = (
            select(Workers.id, Workers.name, Workers.function_id, Function.name)
            .join(Function, Function.id == Workers.function_id)
            .where(
                Workers.turn_id == turn_id,
                Workers.subsidiarie_id == subsidiarie_id,
                Workers.is_active == True,
            )
        )

        workers = session.exec(statement).all()

        workers_with_no_today_scales = []

        for worker in workers:
            # Query para buscar escalas do trabalhador
            statement = select(Scale).where(Scale.worker_id == worker.id)
            worker_scales = session.exec(statement).all()

            # Verificando se a data de hoje está nas escalas do trabalhador
            worker_scales_contains_today = any(
                date.today().strftime("%d-%m-%Y") in scale.date
                for scale in worker_scales
            )

            # Se a data de hoje não for encontrada, adiciona o trabalhador à lista
            if not worker_scales_contains_today:
                workers_with_no_today_scales.append(
                    {
                        "worker_id": worker[0],
                        "worker_name": worker[1],
                        "function_id": worker[2],
                        "function_name": worker[3],
                    }
                )

        return workers_with_no_today_scales


def handle_get_active_workers_by_subsidiarie_and_function(
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


def handle_post_worker(worker: Workers):
    with Session(engine) as session:
        session.add(worker)

        session.commit()

        session.refresh(worker)
    return worker


def handle_deactivate_worker(worker_id: int):
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
