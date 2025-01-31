from datetime import datetime, timedelta

from sqlmodel import Session, select

from database.sqlite import engine
from models.scale import Scale
from models.turn import Turn
from models.workers import Workers
from pyhints.scales import ScalesReportInput


async def handle_generate_scale_days_on_report(
    subsidiarie_id: int, input: ScalesReportInput
):
    with Session(engine) as session:
        turns = session.exec(select(Turn).where(Turn.id.in_([1, 2, 3, 4, 5]))).all()

        first_day = datetime.strptime(input.first_day, "%d-%m-%Y")

        last_day = datetime.strptime(input.last_day, "%d-%m-%Y")

        dias_do_mes = []

        data_atual = first_day

        while data_atual <= last_day:
            dias_do_mes.append(data_atual.strftime("%d-%m-%Y"))

            data_atual += timedelta(days=1)

        all_turns_reports = []

        for turn in turns:
            turn_report = [{"turn_info": turn}]

            for dia_do_mes in dias_do_mes:
                caixas_ao_turno_e_dia = session.exec(
                    select(Scale)
                    .where(Scale.subsidiarie_id == subsidiarie_id)
                    .where(Scale.days_on.contains(dia_do_mes))
                    .where(Scale.worker_turn_id == turn.id)
                    .where(Scale.worker_function_id == 1)
                ).all()

                frentistas_ao_turno_e_dia = session.exec(
                    select(Scale)
                    .where(Scale.subsidiarie_id == subsidiarie_id)
                    .where(Scale.days_on.contains(dia_do_mes))
                    .where(Scale.worker_turn_id == turn.id)
                    .where(Scale.worker_function_id == 4)
                ).all()

                trocadores_ao_turno_e_dia = session.exec(
                    select(Scale)
                    .where(Scale.subsidiarie_id == subsidiarie_id)
                    .where(Scale.days_on.contains(dia_do_mes))
                    .where(Scale.worker_turn_id == turn.id)
                    .where(Scale.worker_function_id == 9)
                ).all()

                turn_report.append(
                    {
                        "date": dia_do_mes,
                        "dados_caixas": [
                            session.get(Workers, caixa.worker_id)
                            for caixa in caixas_ao_turno_e_dia
                        ],
                        "quantidade_caixas": len(caixas_ao_turno_e_dia),
                        "dados_frentistas": [
                            session.get(Workers, frentista.worker_id)
                            for frentista in frentistas_ao_turno_e_dia
                        ],
                        "quantidade_frentistas": len(frentistas_ao_turno_e_dia),
                        "dados_trocadores": [
                            session.get(Workers, trocador.worker_id)
                            for trocador in trocadores_ao_turno_e_dia
                        ],
                        "quantidade_trocadores": len(trocadores_ao_turno_e_dia),
                        "status": (
                            "qtde de colaboradores suficiente"
                            if len(frentistas_ao_turno_e_dia) >= 3
                            and len(trocadores_ao_turno_e_dia) >= 1
                            else "qtde de colaboradores insuficiente"
                        ),
                    }
                )

            all_turns_reports.append(turn_report)

        return all_turns_reports


async def handle_generate_scale_days_off_report(
    subsidiarie_id: int, input: ScalesReportInput
):
    with Session(engine) as session:
        turns = session.exec(select(Turn).where(Turn.id.in_([1, 2, 3, 4, 5]))).all()

        first_day = datetime.strptime(input.first_day, "%d-%m-%Y")

        last_day = datetime.strptime(input.last_day, "%d-%m-%Y")

        dias_do_mes = []

        data_atual = first_day

        while data_atual <= last_day:
            dias_do_mes.append(data_atual.strftime("%d-%m-%Y"))

            data_atual += timedelta(days=1)

        all_turns_reports = []

        for turn in turns:
            turn_report = [{"turn_info": turn}]

            for dia_do_mes in dias_do_mes:
                caixas_ao_turno_e_dia = session.exec(
                    select(Scale)
                    .where(Scale.subsidiarie_id == subsidiarie_id)
                    .where(Scale.days_off.contains(dia_do_mes))
                    .where(Scale.worker_turn_id == turn.id)
                    .where(Scale.worker_function_id == 1)
                ).all()

                frentistas_ao_turno_e_dia = session.exec(
                    select(Scale)
                    .where(Scale.subsidiarie_id == subsidiarie_id)
                    .where(Scale.days_off.contains(dia_do_mes))
                    .where(Scale.worker_turn_id == turn.id)
                    .where(Scale.worker_function_id == 4)
                ).all()

                trocadores_ao_turno_e_dia = session.exec(
                    select(Scale)
                    .where(Scale.subsidiarie_id == subsidiarie_id)
                    .where(Scale.days_off.contains(dia_do_mes))
                    .where(Scale.worker_turn_id == turn.id)
                    .where(Scale.worker_function_id == 9)
                ).all()

                turn_report.append(
                    {
                        "date": dia_do_mes,
                        "dados_caixas": [
                            session.get(Workers, caixa.worker_id)
                            for caixa in caixas_ao_turno_e_dia
                        ],
                        "quantidade_caixas": len(caixas_ao_turno_e_dia),
                        "dados_frentistas": [
                            session.get(Workers, frentista.worker_id)
                            for frentista in frentistas_ao_turno_e_dia
                        ],
                        "quantidade_frentistas": len(frentistas_ao_turno_e_dia),
                        "dados_trocadores": [
                            session.get(Workers, trocador.worker_id)
                            for trocador in trocadores_ao_turno_e_dia
                        ],
                        "quantidade_trocadores": len(trocadores_ao_turno_e_dia),
                        "status": (
                            "quantidade de colaboradores suficiente"
                            if len(frentistas_ao_turno_e_dia) >= 3
                            and len(trocadores_ao_turno_e_dia) >= 1
                            else "quantidade de colaboradores insuficiente"
                        ),
                    }
                )

            all_turns_reports.append(turn_report)

        return all_turns_reports
