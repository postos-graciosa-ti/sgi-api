import calendar
import json
from datetime import date, datetime, timedelta

from fastapi import HTTPException
from sqlmodel import Session, select

from database.sqlite import engine
from models.function import Function
from models.scale import Scale
from models.turn import Turn
from models.workers import Workers
from pyhints.scales import PostScaleInput, PostSomeWorkersScaleInput, ScalesPrintInput


def handle_get_scales_by_subsidiarie_id(subsidiarie_id: int):
    with Session(engine) as session:
        statement = (
            select(Scale)
            .join(Workers, Workers.id == Scale.worker_id)
            .where(Scale.subsidiarie_id == subsidiarie_id)
        )

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
                        "name": worker_function.name,
                    },
                    "turn": {
                        "id": worker_turn.id,
                        "start_time": worker_turn.start_time,
                        "end_time": worker_turn.end_time,
                    },
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


def handle_get_days_off_quantity():
    data_atual = datetime.now()

    ano_atual = data_atual.year

    mes_atual = data_atual.month

    semanas_no_mes = len(calendar.monthcalendar(ano_atual, mes_atual))

    folgas = semanas_no_mes * 1

    return folgas


def handle_get_subsidiarie_scale_to_print(id: int):
    hoje = date.today()

    start_date = (
        hoje - timedelta(days=hoje.weekday() + 1) if hoje.weekday() != 6 else hoje
    )

    end_date = start_date + timedelta(days=6)

    with Session(engine) as session:
        scales_print = []

        scales = session.exec(select(Scale).where(Scale.subsidiarie_id == id)).all()

        for scale in scales:
            worker = session.get(Workers, scale.worker_id)

            valid_days_off = []

            valid_days_on = []

            scale_days_off = eval(scale.days_off)

            scale_days_on = eval(scale.days_on)

            for day_off in scale_days_off:
                day_str = day_off.get("date") if isinstance(day_off, dict) else day_off

                if not day_str:
                    continue

                try:
                    day_date = datetime.strptime(day_str, "%d-%m-%Y").date()

                except ValueError:
                    continue

                if start_date <= day_date <= end_date:
                    valid_days_off.append(day_date)

            for day_on in scale_days_on:
                day_str = day_on.get("date") if isinstance(day_on, dict) else day_on

                if not day_str:
                    continue

                try:
                    day_date = datetime.strptime(day_str, "%d-%m-%Y").date()

                except ValueError:
                    continue

                if start_date <= day_date <= end_date:
                    valid_days_on.append(day_date)

            if valid_days_off or valid_days_on:
                scales_print.append(
                    {
                        "worker": worker,
                        "days_on": valid_days_on,
                        "days_off": valid_days_off,
                        "start_date": start_date,
                        "end_date": end_date,
                    }
                )

    return scales_print


def handle_post_scale(form_data: PostScaleInput):
    try:
        # Converte a string recebida para uma lista
        form_data.days_off = eval(form_data.days_off)

        # Converte as datas de início e fim para objetos datetime
        first_day = datetime.strptime(form_data.first_day, "%d-%m-%Y")
        last_day = datetime.strptime(form_data.last_day, "%d-%m-%Y")

        # Cria uma lista com todas as datas do período (ordenada cronologicamente)
        dias_do_mes = []
        data_atual = first_day
        while data_atual <= last_day:
            dias_do_mes.append(data_atual.strftime("%d-%m-%Y"))
            data_atual += timedelta(days=1)

        # Abre a sessão com o banco
        with Session(engine) as session:
            # Verifica se o trabalhador existe
            worker = session.exec(
                select(Workers).where(Workers.id == form_data.worker_id)
            ).first()
            if not worker:
                raise HTTPException(
                    status_code=400, detail="Trabalhador não encontrado."
                )

            # Busca uma escala existente para o mesmo trabalhador e subsidiária
            existing_scale = session.exec(
                select(Scale).where(
                    Scale.worker_id == form_data.worker_id,
                    Scale.subsidiarie_id == form_data.subsidiarie_id,
                )
            ).first()

            # Inicialmente, os novos days off serão baseados no form_data
            merged_days_off_dates = set(form_data.days_off)

            # Se já existir uma escala, mescla os days off já salvos com os novos
            if existing_scale and existing_scale.days_off:
                old_days_off = json.loads(existing_scale.days_off)
                old_days_off_dates = [d["date"] for d in old_days_off]
                merged_days_off_dates.update(old_days_off_dates)

            # Converte para lista e ordena as datas
            merged_days_off_dates = sorted(
                list(merged_days_off_dates),
                key=lambda d: datetime.strptime(d, "%d-%m-%Y"),
            )

            # Garante que existam days off após a mesclagem
            if not merged_days_off_dates:
                raise HTTPException(
                    status_code=400, detail="Não é possível salvar sem dias de folga."
                )

            # Calcula os dias que não são de folga com base na lista mesclada
            merged_dias_sem_folga = [
                dia for dia in dias_do_mes if dia not in merged_days_off_dates
            ]

            # As listas days off e days on já ficam ordenadas por data
            merged_days_off_with_weekday = [
                {
                    "date": date,
                    "weekday": datetime.strptime(date, "%d-%m-%Y").strftime("%A"),
                }
                for date in merged_days_off_dates
            ]
            merged_days_on_with_weekday = [
                {
                    "date": date,
                    "weekday": datetime.strptime(date, "%d-%m-%Y").strftime("%A"),
                }
                for date in merged_dias_sem_folga
            ]

            # Calcula as proporções e verifica se há mais de 8 dias consecutivos sem folga
            count = 0
            merged_proporcoes = []
            tem_mais_de_oito_dias_consecutivos = False
            for dia in dias_do_mes:
                count += 1
                if count > 8:
                    tem_mais_de_oito_dias_consecutivos = True
                if dia in merged_days_off_dates:
                    merged_proporcoes.append(
                        {
                            "data": dia,
                            "weekday": datetime.strptime(dia, "%d-%m-%Y").strftime(
                                "%A"
                            ),
                            "proporcao": f"{count-1}x1",
                        }
                    )
                    count = 0

            # Se a escala já existe, atualiza os campos mesclando os dados;
            # caso contrário, cria uma nova escala.
            if existing_scale:
                existing_scale.days_off = json.dumps(merged_days_off_with_weekday)
                existing_scale.days_on = json.dumps(merged_days_on_with_weekday)
                existing_scale.need_alert = tem_mais_de_oito_dias_consecutivos
                existing_scale.proportion = json.dumps(merged_proporcoes)
                existing_scale.ilegal_dates = form_data.ilegal_dates
            else:
                existing_scale = Scale(
                    worker_id=form_data.worker_id,
                    subsidiarie_id=form_data.subsidiarie_id,
                    days_off=json.dumps(merged_days_off_with_weekday),
                    days_on=json.dumps(merged_days_on_with_weekday),
                    need_alert=tem_mais_de_oito_dias_consecutivos,
                    proportion=json.dumps(merged_proporcoes),
                    ilegal_dates=form_data.ilegal_dates,
                    worker_function_id=form_data.worker_function_id,
                    worker_turn_id=form_data.worker_turn_id,
                )
                session.add(existing_scale)

            session.commit()
            session.refresh(existing_scale)

            # Prepara a resposta: extrai apenas as datas de days off
            sla = []
            existing_scale_days_off = json.loads(existing_scale.days_off)
            for day_off in existing_scale_days_off:
                sla.append(day_off["date"])

            return {"days_off": sla, "ilegal_dates": eval(existing_scale.ilegal_dates)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def handle_post_some_workers_scale(form_data: PostSomeWorkersScaleInput):
    try:
        # Converte a string recebida para uma lista
        form_data.days_off = eval(form_data.days_off)

        # Converte as datas de início e fim para objetos datetime
        first_day = datetime.strptime(form_data.first_day, "%d-%m-%Y")
        last_day = datetime.strptime(form_data.last_day, "%d-%m-%Y")

        # Cria uma lista com todas as datas do período (ordenada cronologicamente)
        dias_do_mes = []
        data_atual = first_day
        while data_atual <= last_day:
            dias_do_mes.append(data_atual.strftime("%d-%m-%Y"))
            data_atual += timedelta(days=1)

        results = []

        with Session(engine) as session:
            # Itera sobre a lista de worker IDs (supondo que o input agora contenha "worker_ids")
            form_data.worker_ids = eval(form_data.worker_ids)

            for worker_id in form_data.worker_ids:
                # Verifica se o trabalhador existe
                worker = session.exec(
                    select(Workers).where(Workers.id == worker_id)
                ).first()
                if not worker:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Trabalhador {worker_id} não encontrado.",
                    )

                # Busca a escala existente para o mesmo worker e subsidiária
                existing_scale = session.exec(
                    select(Scale).where(
                        Scale.worker_id == worker_id,
                        Scale.subsidiarie_id == form_data.subsidiarie_id,
                    )
                ).first()

                # Inicia a mesclagem dos "days off": utiliza os novos e, se existir, adiciona os já salvos
                merged_days_off_dates = set(form_data.days_off)
                if existing_scale and existing_scale.days_off:
                    old_days_off = json.loads(existing_scale.days_off)
                    old_days_off_dates = [d["date"] for d in old_days_off]
                    merged_days_off_dates.update(old_days_off_dates)

                # Converte para lista e ordena as datas
                merged_days_off_dates = sorted(
                    list(merged_days_off_dates),
                    key=lambda d: datetime.strptime(d, "%d-%m-%Y"),
                )

                # Garante que existam days off após a mesclagem
                if not merged_days_off_dates:
                    raise HTTPException(
                        status_code=400,
                        detail="Não é possível salvar sem dias de folga.",
                    )

                # Calcula os dias que não são de folga (days on) a partir da lista ordenada
                merged_dias_sem_folga = [
                    dia for dia in dias_do_mes if dia not in merged_days_off_dates
                ]

                # Gera as listas com weekday para days off e days on
                merged_days_off_with_weekday = [
                    {
                        "date": date,
                        "weekday": datetime.strptime(date, "%d-%m-%Y").strftime("%A"),
                    }
                    for date in merged_days_off_dates
                ]
                merged_days_on_with_weekday = [
                    {
                        "date": date,
                        "weekday": datetime.strptime(date, "%d-%m-%Y").strftime("%A"),
                    }
                    for date in merged_dias_sem_folga
                ]

                # Calcula as proporções e verifica se há mais de 8 dias consecutivos sem folga
                count = 0
                merged_proporcoes = []
                tem_mais_de_oito_dias_consecutivos = False
                for dia in dias_do_mes:
                    count += 1
                    if count > 8:
                        tem_mais_de_oito_dias_consecutivos = True
                    if dia in merged_days_off_dates:
                        merged_proporcoes.append(
                            {
                                "data": dia,
                                "weekday": datetime.strptime(dia, "%d-%m-%Y").strftime(
                                    "%A"
                                ),
                                "proporcao": f"{count-1}x1",
                            }
                        )
                        count = 0

                # Atualiza a escala se já existir; caso contrário, cria uma nova
                if existing_scale:
                    existing_scale.days_off = json.dumps(merged_days_off_with_weekday)
                    existing_scale.days_on = json.dumps(merged_days_on_with_weekday)
                    existing_scale.need_alert = tem_mais_de_oito_dias_consecutivos
                    existing_scale.proportion = json.dumps(merged_proporcoes)
                    existing_scale.ilegal_dates = form_data.ilegal_dates
                else:
                    new_scale = Scale(
                        worker_id=worker_id,
                        subsidiarie_id=form_data.subsidiarie_id,
                        days_off=json.dumps(merged_days_off_with_weekday),
                        days_on=json.dumps(merged_days_on_with_weekday),
                        need_alert=tem_mais_de_oito_dias_consecutivos,
                        proportion=json.dumps(merged_proporcoes),
                        ilegal_dates=form_data.ilegal_dates,
                        worker_function_id=worker.function_id,
                        worker_turn_id=worker.turn_id,
                    )
                    session.add(new_scale)
                    existing_scale = new_scale

                session.commit()
                session.refresh(existing_scale)

                # Prepara os dados de retorno para este worker
                existing_scale_days_off = json.loads(existing_scale.days_off)
                days_off_list = [d["date"] for d in existing_scale_days_off]

                results.append(
                    {
                        "worker_id": worker_id,
                        "days_off": days_off_list,
                        "ilegal_dates": eval(existing_scale.ilegal_dates),
                    }
                )

        return {"results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def handle_handle_scale(form_data: PostScaleInput):
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

        all_dates = sorted(
            dias_sem_folga + form_data.days_off,
            key=lambda d: datetime.strptime(d, "%d-%m-%Y"),
        )

        count = 0

        proporcoes = []

        tem_mais_de_oito_dias_consecutivos = False

        for dia in dias_do_mes:
            count += 1

            if count > 8:
                tem_mais_de_oito_dias_consecutivos = True

            if dia in form_data.days_off:
                proporcoes.append(
                    {
                        "data": dia,
                        "weekday": datetime.strptime(dia, "%d-%m-%Y").strftime("%A"),
                        "proporcao": f"{count-1}x1",
                    }
                )

                count = 0

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
            worker = session.exec(
                select(Workers).where(Workers.id == form_data.worker_id)
            ).first()

            if not worker:
                raise HTTPException(
                    status_code=400, detail="Trabalhador não encontrado."
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
                    worker_function_id=form_data.worker_function_id,
                    worker_turn_id=form_data.worker_turn_id,
                )
                session.add(existing_scale)

            session.commit()

            session.refresh(existing_scale)

        sla = []

        existing_scale_days_off = json.loads(existing_scale.days_off)

        for day_off in existing_scale_days_off:
            sla.append(day_off["date"])

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


from fastapi import HTTPException

def handle_post_subsidiarie_scale_to_print(id: int, scales_print_input: ScalesPrintInput):
    start_date = datetime.strptime(scales_print_input.start_date, "%d-%m-%Y").date()
    end_date = datetime.strptime(scales_print_input.end_date, "%d-%m-%Y").date()

    workers_ids_filter = set(scales_print_input.workers_ids) if scales_print_input.workers_ids else None
    scales_print = []

    with Session(engine) as session:
        # Get all scales with workers in the specified turn (using join)
        scales = session.exec(
            select(Scale)
            .join(Workers, Scale.worker_id == Workers.id)
            .where(Scale.subsidiarie_id == id)
            .where(Workers.turn_id == scales_print_input.turn_id)
        ).all()

        # Dictionary to track day off conflicts
        day_off_conflicts = {}

        for scale in scales:
            if workers_ids_filter and scale.worker_id not in workers_ids_filter:
                continue

            worker = session.get(Workers, scale.worker_id)
            if not worker:
                continue

            scale_days_off = json.loads(scale.days_off) if isinstance(scale.days_off, str) else scale.days_off or []
            
            # Check for day off conflicts
            for day in scale_days_off:
                if isinstance(day, dict) and "date" in day:
                    try:
                        date_obj = datetime.strptime(day["date"], "%d-%m-%Y").date()
                        if start_date <= date_obj <= end_date:
                            conflict_key = (day["date"], worker.function_id)
                            
                            if conflict_key not in day_off_conflicts:
                                day_off_conflicts[conflict_key] = []
                            
                            day_off_conflicts[conflict_key].append({
                                "worker_id": worker.id,
                                "worker_name": worker.name  # Assuming Workers has a 'name' field
                            })
                    except:
                        continue

        # Check for conflicts and prepare error message if found
        conflict_messages = []
        for (date_str, function_id), workers in day_off_conflicts.items():
            if len(workers) > 1:
                worker_list = ", ".join([f"{w['worker_name']} (ID: {w['worker_id']})" for w in workers])
                conflict_messages.append(
                    f"Conflito no dia {date_str} (função ID: {function_id}): {worker_list}"
                )

        if conflict_messages:
            error_msg = "Conflito de dias off encontrados:\n" + "\n".join(conflict_messages)
            raise HTTPException(
                status_code=400,
                detail=error_msg
            )

        # Process scales if no conflicts found
        for scale in scales:
            if workers_ids_filter and scale.worker_id not in workers_ids_filter:
                continue

            worker = session.get(Workers, scale.worker_id)
            if not worker:
                continue

            scale_days_off = json.loads(scale.days_off) if isinstance(scale.days_off, str) else scale.days_off or []
            scale_days_on = json.loads(scale.days_on) if isinstance(scale.days_on, str) else scale.days_on or []
            scale_proportion = json.loads(scale.proportion) if isinstance(scale.proportion, str) else scale.proportion or []

            valid_days_off = [
                datetime.strptime(day["date"], "%d-%m-%Y").date()
                for day in scale_days_off if isinstance(day, dict) and "date" in day
                and start_date <= datetime.strptime(day["date"], "%d-%m-%Y").date() <= end_date
            ]

            valid_days_on = [
                datetime.strptime(day["date"], "%d-%m-%Y").date()
                for day in scale_days_on if isinstance(day, dict) and "date" in day
                and start_date <= datetime.strptime(day["date"], "%d-%m-%Y").date() <= end_date
            ]

            valid_proportion = [
                day
                for day in scale_proportion if isinstance(day, dict)
                and start_date <= datetime.strptime(day["data"], "%d-%m-%Y").date() <= end_date
            ]

            scales_print.append({
                "worker": worker,
                "days_on": valid_days_on,
                "days_off": valid_days_off,
                "proportion": valid_proportion,
                "start_date": start_date,
                "end_date": end_date,
            })

    return scales_print