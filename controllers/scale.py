import json
from datetime import datetime

from fastapi import HTTPException
from sqlmodel import Session, select

from database.sqlite import engine
from models.function import Function
from models.scale import Scale
from models.turn import Turn
from models.workers import Workers
from pyhints.scales import GetScalesByDate


def handle_get_scale_by_subsidiarie_id(subsidiarie_id: int):
    with Session(engine) as session:
        statement = select(Scale).where(Scale.subsidiarie_id == subsidiarie_id)

        scales = session.exec(statement).all()

        if not scales:
            raise HTTPException(
                status_code=404, detail="No scales found for the given subsidiary."
            )

        result = []

        for scale in scales:
            workers_on = json.loads(scale.workers_on)

            workers_off = json.loads(scale.workers_off)

            workers_on_data = [
                session.get(Workers, worker_id) for worker_id in workers_on
            ]

            workers_off_data = [
                session.get(Workers, worker_id) for worker_id in workers_off
            ]

            def format_worker(worker):
                if worker:
                    function = session.get(Function, worker.function_id)

                    turn = session.get(Turn, worker.turn_id)

                    return {
                        "id": worker.id,
                        "name": worker.name,
                        "function": {
                            "id": function.id if function else None,
                            "name": function.name if function else "Unknown",
                        },
                        "turn": {
                            "id": turn.id if turn else None,
                            "name": turn.name if turn else "Unknown",
                        },
                    }
                return None

            result.append(
                {
                    "scale_id": scale.id,
                    "date": scale.date,
                    "workers_on": [
                        format_worker(worker) for worker in workers_on_data if worker
                    ],
                    "workers_off": [
                        format_worker(worker) for worker in workers_off_data if worker
                    ],
                }
            )

    return result


def handle_get_scale_by_date(formData: GetScalesByDate):
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


def handle_post_scale(formData: Scale):
    formData.date = datetime.strptime(formData.date, "%d/%m/%Y").date()

    with Session(engine) as session:
        session.add(formData)

        session.commit()

        session.refresh(formData)
    return formData


def handle_delete_scale(id: int):
    with Session(engine) as session:
        scale = session.get(Scale, id)

        session.delete(scale)

        session.commit()
    return {"message": "Escala deletada com sucesso"}
