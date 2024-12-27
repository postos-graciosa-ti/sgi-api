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


def handle_get_scales_by_subsidiarie_and_worker_id(subsidiarie_id: int, worker_id: int):
    with Session(engine) as session:
        statement = (
            select(Scale)
            .where(Scale.subsidiarie_id == subsidiarie_id)
            .where(Scale.worker_id == worker_id)
        )

        scales_by_subsidiarie_and_worker_id = session.exec(statement).first()

    return eval(scales_by_subsidiarie_and_worker_id.days_off)


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
            else:
                existing_scale = Scale(
                    worker_id=form_data.worker_id,
                    subsidiarie_id=form_data.subsidiarie_id,
                    days_on=json.dumps(days_on_with_weekday),
                    days_off=json.dumps(days_off_with_weekday),
                    need_alert=tem_mais_de_oito_dias_consecutivos,
                    proportion=json.dumps(proporcoes),
                )

                session.add(existing_scale)

            session.commit()
            
            session.refresh(existing_scale)

        sla = []

        existing_scale_days_off = json.loads(existing_scale.days_off)

        for day_off in existing_scale_days_off:
            sla.append(day_off["date"])

        return sla

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def handle_delete_scale(scale_id: int, subsidiarie_id: int):
    with Session(engine) as session:
        session.delete(session.get(Scale, scale_id))

        session.commit()

        statement = select(Scale).where(Scale.subsidiarie_id == subsidiarie_id)

        all_scales_by_subsidiarie = session.exec(statement).all()

    return all_scales_by_subsidiarie
