from datetime import datetime, timedelta

from sqlmodel import Session, func, select

from database.sqlite import engine
from models.function import Function
from models.jobs import Jobs
from models.scale import Scale
from models.workers import Workers


async def get_workers_without_scales(subsidiarie_id):
    with Session(engine) as session:
        all_workers = session.exec(
            select(Workers).where(Workers.subsidiarie_id == subsidiarie_id)
        ).all()

        all_scales = session.exec(
            select(Scale).where(Scale.subsidiarie_id == subsidiarie_id)
        ).all()

        workers_with_scales = {scale.worker_id for scale in all_scales}

        workers_without_scale = [
            worker for worker in all_workers if worker.id not in workers_with_scales
        ]

        return workers_without_scale


async def get_workers_with_less_than_ideal_days_off(subsidiarie_id):
    with Session(engine) as session:
        ideal_days_off = 5

        workers = session.exec(
            select(Workers)
            .join(Scale, Workers.id == Scale.worker_id)
            .where(Scale.subsidiarie_id == subsidiarie_id)
            .where(func.json_array_length(Scale.days_off) < ideal_days_off)
        ).all()

        return {"workers": workers, "ideal_days_off": ideal_days_off}


async def get_open_jobs(subsidiarie_id):
    with Session(engine) as session:
        jobs = session.exec(
            select(Jobs).where(Jobs.subsidiarie_id == subsidiarie_id)
        ).all()

        return jobs


async def handle_get_subsidiarie_notifications(id: int):
    workers_without_scales = await get_workers_without_scales(id)

    open_jobs = await get_open_jobs(id)

    workers_with_less_than_ideal_days_off = (
        await get_workers_with_less_than_ideal_days_off(id)
    )

    return {
        "workers_without_scales": workers_without_scales,
        "open_jobs": open_jobs,
        "workers_with_less_than_ideal_days_off": workers_with_less_than_ideal_days_off[
            "workers"
        ],
        "ideal_days_off": workers_with_less_than_ideal_days_off["ideal_days_off"],
    }


async def handle_get_subsidiaries_status(id: int):
    with Session(engine) as session:
        frentistas = session.exec(
            select(Workers)
            .where(Workers.subsidiarie_id == id)
            .where(Workers.function_id == 4)
        ).all()

        frentistas_caixa = session.exec(
            select(Workers)
            .where(Workers.subsidiarie_id == id)
            .where(Workers.function_id == 2)
        ).all()

        caixas = session.exec(
            select(Workers)
            .where(Workers.subsidiarie_id == id)
            .where(Workers.function_id == 1)
        ).all()

        trocadores = session.exec(
            select(Workers)
            .where(Workers.subsidiarie_id == id)
            .where(Workers.function_id == 9)
        ).all()

        frentistas_ideal_quantity = session.get(Function, 4).ideal_quantity

        frentistas_diference = frentistas_ideal_quantity - len(frentistas)

        trocadores_ideal_quantity = session.get(Function, 9).ideal_quantity

        trocadores_diference = trocadores_ideal_quantity - len(trocadores)

        return {
            "dados_frentistas": frentistas,
            "quantidade_frentistas": len(frentistas),
            "frentistas_ideal_quantity": frentistas_ideal_quantity,
            "frentistas_diference": frentistas_diference,
            # "status_frentistas": [
            #     (
            #         "quantidade suficiente"
            #         if session.get(Function, frentista.function_id).ideal_quantity
            #         == len(frentistas)
            #         else "quantidade insuficiente"
            #     )
            #     for frentista in frentistas
            # ],
            "dados_frentistas_caixa": frentistas_caixa,
            "quantidade_frentistas_caixa": len(frentistas_caixa),
            "dados_caixas": caixas,
            "quantidade_caixas": len(caixas),
            "dados_trocadores": trocadores,
            "quantidade_trocadores": len(trocadores),
            "trocadores_ideal_quantity": trocadores_ideal_quantity,
            "trocadores_diference": trocadores_diference,
        }
