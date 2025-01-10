import json
import locale
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlmodel import Session, select

from database.sqlite import engine
from models.function import Function
from models.scale import Scale
from models.turn import Turn
from models.workers import Workers
from pyhints.scales import GetScalesByDate, PostScaleInput

# locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")


def handle_get_scales_by_subsidiarie_id(subsidiarie_id: int):
    # with Session(engine) as session:
    #     results = session.exec(
    #         select(Scale, Workers)
    #         .join(Workers, Workers.id == Scale.worker_id)
    #         .where(Scale.subsidiarie_id == subsidiarie_id)
    #     ).all()

    #     options = []

    #     for result in results:
    #         options.append({"scale": result[0], "worker": result[1]})

    #     for option in options:
    #         option["worker"].function_id = session.get(
    #             Function, option["worker"].function_id
    #         )

    #     return options

    with Session(engine) as session:
        statement = select(Scale).join(Workers, Workers.id == Scale.worker_id).where(Scale.subsidiarie_id == subsidiarie_id)

        scales_by_subsidiarie = session.exec(statement).all()

        format_scales = []

        for scale in scales_by_subsidiarie:
            worker = session.get(Workers, scale.worker_id)
            worker_function = session.get(Function, worker.function_id)
            worker_turn = session.get(Turn, worker.turn_id)
            
            format_scale = {
                "id": scale.id,
                "worker": {
                    "id": worker.id,
                    "name": worker.name,
                    "function": {
                        "id": worker_function.id,
                        "name": worker_function.name
                    },
                    "turn": {
                        "id": worker_turn.id,
                        "start_time": worker_turn.start_time,
                        "end_time": worker_turn.end_time
                    }
                },
                "days_on": eval(scale.days_on),
                "days_off": eval(scale.days_off),
                "need_alert": scale.need_alert,
                "proportion": scale.proportion,
                "ilegal_dates": eval(scale.ilegal_dates),
            }

            format_scales.append(format_scale)

    return format_scales


def handle_get_scales_by_subsidiarie_and_worker_id(subsidiarie_id: int, worker_id: int):
    with Session(engine) as session:
        statement = (
            select(Scale)
            .where(Scale.subsidiarie_id == subsidiarie_id)
            .where(Scale.worker_id == worker_id)
        )

        scales_by_subsidiarie_and_worker_id = session.exec(statement).first()

    # return eval(scales_by_subsidiarie_and_worker_id.days_off)

    return {
        "days_off": eval(scales_by_subsidiarie_and_worker_id.days_off),
        "ilegal_dates": eval(scales_by_subsidiarie_and_worker_id.ilegal_dates),
    }


def handle_post_scale(form_data: PostScaleInput):
    try:
        form_data.days_off = eval(form_data.days_off)

        first_day = datetime.strptime(form_data.first_day, "%d-%m-%Y")

        last_day = datetime.strptime(form_data.last_day, "%d-%m-%Y")

        dias_do_mes = []

        data_atual = first_day

        while data_atual <= last_day:
            dias_do_mes.append(data_atual.strftime("%d-%m-%Y"))
            data_atual += timedelta(days=1)

        dias_sem_folga = [dia for dia in dias_do_mes if dia not in form_data.days_off]

        all_dates = sorted(dias_sem_folga + form_data.days_off)

        options = [
            {"dayOff": date in form_data.days_off, "value": date} for date in all_dates
        ]

        dias_consecutivos = []
        contador = 0
        tem_mais_de_oito_dias_consecutivos = False

        for dia in options:
            if dia["dayOff"]:
                dias_consecutivos.append({"dias": contador, "dataFolga": dia["value"]})
                contador = 0
            else:
                contador += 1
                if contador > 8:
                    tem_mais_de_oito_dias_consecutivos = True

        proporcoes = [
            {
                "folga": idx + 1,
                "data": item["dataFolga"],
                "weekday": datetime.strptime(item["dataFolga"], "%d-%m-%Y").strftime(
                    "%A"
                ),
                "proporcao": f"{item['dias']}x1",
            }
            for idx, item in enumerate(dias_consecutivos)
        ]

        if not form_data.days_off:
            raise HTTPException(
                status_code=400, detail="Não é possível salvar sem dias de folga."
            )

        days_off_with_weekday = [
            {
                "date": date,
                "weekday": datetime.strptime(date, "%d-%m-%Y").strftime("%A"),
            }
            for date in form_data.days_off
        ]

        days_on_with_weekday = [
            {
                "date": date,
                "weekday": datetime.strptime(date, "%d-%m-%Y").strftime("%A"),
            }
            for date in dias_sem_folga
        ]

        with Session(engine) as session:
            # Obter o turno do trabalhador atual
            worker = session.exec(
                select(Workers).where(Workers.id == form_data.worker_id)
            ).first()

            if not worker:
                raise HTTPException(
                    status_code=400, detail="Trabalhador não encontrado."
                )

            worker_turn_id = worker.turn_id  # Obtém o turn_id do trabalhador

            for day_off in form_data.days_off:
                existing_workers = session.exec(
                    select(Scale)
                    .join(
                        Workers, Scale.worker_id == Workers.id
                    )  # Juntar com a tabela Worker
                    .where(
                        Scale.subsidiarie_id == form_data.subsidiarie_id,  # Mesmo local
                        Workers.turn_id == worker_turn_id,  # Mesmo turno
                        Scale.days_off.contains(
                            f'"{day_off}"'
                        ),  # Dia de folga em comum
                        Scale.worker_id
                        != form_data.worker_id,  # Ignorar o próprio trabalhador
                    )
                ).all()

                if existing_workers:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Já existem trabalhadores no turno '{worker_turn_id}' com folga no dia {day_off}.",
                    )

            existing_scale = session.exec(
                select(Scale).where(
                    Scale.worker_id == form_data.worker_id,
                    Scale.subsidiarie_id == form_data.subsidiarie_id,
                )
            ).first()

            if existing_scale:
                existing_scale.days_on = json.dumps(days_on_with_weekday)
                existing_scale.days_off = json.dumps(days_off_with_weekday)
                existing_scale.need_alert = tem_mais_de_oito_dias_consecutivos
                existing_scale.proportion = json.dumps(proporcoes)
                existing_scale.ilegal_dates = form_data.ilegal_dates
            else:
                existing_scale = Scale(
                    worker_id=form_data.worker_id,
                    subsidiarie_id=form_data.subsidiarie_id,
                    days_on=json.dumps(days_on_with_weekday),
                    days_off=json.dumps(days_off_with_weekday),
                    need_alert=tem_mais_de_oito_dias_consecutivos,
                    proportion=json.dumps(proporcoes),
                    ilegal_dates=form_data.ilegal_dates,
                )

                session.add(existing_scale)

            session.commit()

            session.refresh(existing_scale)

        sla = []

        existing_scale_days_off = json.loads(existing_scale.days_off)

        for day_off in existing_scale_days_off:
            sla.append(day_off["date"])

        # return sla

        return {"days_off": sla, "ilegal_dates": eval(existing_scale.ilegal_dates)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def handle_delete_scale(scale_id: int, subsidiarie_id: int):
    with Session(engine) as session:
        session.delete(session.get(Scale, scale_id))

        session.commit()

        statement = select(Scale).where(Scale.subsidiarie_id == subsidiarie_id)

        all_scales_by_subsidiarie = session.exec(statement).all()

    return all_scales_by_subsidiarie
