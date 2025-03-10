from datetime import datetime, timedelta

from sqlmodel import Session, select

from database.sqlite import engine
from models.function import Function
from models.scale import Scale
from models.turn import Turn
from models.workers import Workers
from pyhints.scales import ScalesReportInput


async def handle_generate_scale_days_on_report(
    subsidiarie_id: int, input: ScalesReportInput
):
    with Session(engine) as session:
        # Buscar funções de uma vez
        functions = session.exec(
            select(Function)
            .where(Function.subsidiarie_id == subsidiarie_id)
            .where(
                Function.name.in_(
                    [
                        "Operador(a) de Caixa I",
                        "Frentista I",
                        "Trocador de Óleo / Frentista II",
                    ]
                )
            )
        ).all()

        caixas_id = next(f for f in functions if f.name == "Operador(a) de Caixa I")
        frentistas_id = next(f for f in functions if f.name == "Frentista I")
        trocadores_id = next(
            f for f in functions if f.name == "Trocador de Óleo / Frentista II"
        )

        # Buscar todos os turnos de uma vez
        turns = session.exec(
            select(Turn).where(Turn.subsidiarie_id == subsidiarie_id)
        ).all()

        # Parse das datas
        first_day = datetime.strptime(input.first_day, "%d-%m-%Y")
        last_day = datetime.strptime(input.last_day, "%d-%m-%Y")

        # Criando a lista de dias
        dias_do_mes = []
        data_atual = first_day
        while data_atual <= last_day:
            dias_do_mes.append(data_atual.strftime("%d-%m-%Y"))
            data_atual += timedelta(days=1)

        # Coletar escalas para os três tipos de função de uma vez
        scales = session.exec(
            select(Scale)
            .where(Scale.subsidiarie_id == subsidiarie_id)
            .where(
                Scale.worker_function_id.in_(
                    [caixas_id.id, frentistas_id.id, trocadores_id.id]
                )
            )
            .where(Scale.worker_turn_id.in_([turn.id for turn in turns]))
        ).all()

        # Organizar as escalas por turno, função e dia
        all_turns_reports = []
        for turn in turns:
            turn_report = [{"turn_info": turn}]
            for dia_do_mes in dias_do_mes:
                # Filtrar escalas para o dia e turno atuais
                turn_scales = [
                    scale
                    for scale in scales
                    if scale.worker_turn_id == turn.id and dia_do_mes in scale.days_on
                ]

                caixas_ao_turno_e_dia = [
                    scale
                    for scale in turn_scales
                    if scale.worker_function_id == caixas_id.id
                ]
                frentistas_ao_turno_e_dia = [
                    scale
                    for scale in turn_scales
                    if scale.worker_function_id == frentistas_id.id
                ]
                trocadores_ao_turno_e_dia = [
                    scale
                    for scale in turn_scales
                    if scale.worker_function_id == trocadores_id.id
                ]

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
        functions = session.exec(
            select(Function)
            .where(Function.subsidiarie_id == subsidiarie_id)
            .where(
                Function.name.in_(
                    [
                        "Operador(a) de Caixa I",
                        "Frentista I",
                        "Trocador de Óleo / Frentista II",
                    ]
                )
            )
        ).all()

        caixas_id = next(f for f in functions if f.name == "Operador(a) de Caixa I")

        frentistas_id = next(f for f in functions if f.name == "Frentista I")

        trocadores_id = next(
            f for f in functions if f.name == "Trocador de Óleo / Frentista II"
        )

        turns = session.exec(
            select(Turn).where(Turn.subsidiarie_id == subsidiarie_id)
        ).all()

        first_day = datetime.strptime(input.first_day, "%d-%m-%Y")

        last_day = datetime.strptime(input.last_day, "%d-%m-%Y")

        dias_do_mes = []

        data_atual = first_day

        while data_atual <= last_day:
            dias_do_mes.append(data_atual.strftime("%d-%m-%Y"))

            data_atual += timedelta(days=1)

        scales = session.exec(
            select(Scale)
            .where(Scale.subsidiarie_id == subsidiarie_id)
            .where(
                Scale.worker_function_id.in_(
                    [caixas_id.id, frentistas_id.id, trocadores_id.id]
                )
            )
            .where(Scale.worker_turn_id.in_([turn.id for turn in turns]))
        ).all()

        all_turns_reports = []

        for turn in turns:
            turn_report = [{"turn_info": turn}]

            for dia_do_mes in dias_do_mes:
                turn_scales = [
                    scale
                    for scale in scales
                    if scale.worker_turn_id == turn.id and dia_do_mes in scale.days_off
                ]

                caixas_ao_turno_e_dia = [
                    scale
                    for scale in turn_scales
                    if scale.worker_function_id == caixas_id.id
                ]

                frentistas_ao_turno_e_dia = [
                    scale
                    for scale in turn_scales
                    if scale.worker_function_id == frentistas_id.id
                ]

                trocadores_ao_turno_e_dia = [
                    scale
                    for scale in turn_scales
                    if scale.worker_function_id == trocadores_id.id
                ]

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
