import bisect
import os
import re
from datetime import datetime, time
from functools import reduce
from pathlib import Path

import pandas as pd
from fastapi import File, UploadFile
from sqlmodel import Session, select

from database.sqlite import engine
from functions.excel import convert_to_time, extract_turn_info
from models.function import Function
from models.turn import Turn
from models.user import User
from models.workers import Workers


async def handle_excel_scraping(file: UploadFile = File(...)):
    UPLOAD_DIR = "uploads"
    Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

    file_location = os.path.join(UPLOAD_DIR, file.filename)

    # Salva o arquivo enviado
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Lê o arquivo Excel
    df = pd.read_excel(file_location)

    # Filtra os colaboradores do Posto Graciosa (1º) que estão ativos
    colaboradores_posto_graciosa = df[
        (df["Unidade"] == "Posto Graciosa (1º)") & (df["Status(F)"] == "Ativo")
    ]

    # Seleciona as colunas desejadas
    colaboradores_nome_email = colaboradores_posto_graciosa[
        ["Nome do Colaborador", "Cargo Atual", "Turno de Trabalho"]
    ]

    # Substitui valores NaN por None
    colaboradores_nome_email = colaboradores_nome_email.where(
        pd.notna(colaboradores_nome_email), None
    )

    # Converte o DataFrame para uma lista de dicionários
    colaboradores_list = colaboradores_nome_email.to_dict(orient="records")

    # Expressão regular para separar os horários do turno
    regex = r"^(.*)-(.*)$"

    # Cria ou atualiza os registros no banco de dados
    with Session(engine) as session:
        for colaborador in colaboradores_list:
            # Verifica se o turno já existe
            exist_turn = session.execute(
                select(Turn).where(Turn.name == colaborador["Turno de Trabalho"])
            ).first()

            if not exist_turn:
                turn_parts = re.match(regex, colaborador["Turno de Trabalho"])
                if turn_parts:
                    turn_start_time = datetime.strptime(
                        turn_parts.group(1).strip(), "%H:%M"
                    ).time()
                    turn_end_time = datetime.strptime(
                        turn_parts.group(2).strip(), "%H:%M"
                    ).time()
                    turn_start_interval_time = time(0, 0)
                    turn_end_interval_time = time(0, 0)
                    turn = Turn(
                        name=colaborador["Turno de Trabalho"],
                        start_time=turn_start_time,
                        start_interval_time=turn_start_interval_time,
                        end_time=turn_end_time,
                        end_interval_time=turn_end_interval_time,
                    )
                    session.add(turn)

            # Verifica se a função já existe
            exist_function = session.execute(
                select(Function).where(Function.name == colaborador["Cargo Atual"])
            ).first()
            if not exist_function:
                function = Function(
                    name=colaborador["Cargo Atual"],
                    description=colaborador["Cargo Atual"],
                    subsidiarie_id=1,
                )
                session.add(function)

            # Verifica se o worker já existe
            exist_worker = session.exec(
                select(Workers).where(Workers.name == colaborador["Nome do Colaborador"])
            ).first()
            if not exist_worker:
                worker_function = session.exec(
                    select(Function).where(Function.name == colaborador["Cargo Atual"])
                ).first()
                worker_turn = session.exec(
                    select(Turn).where(Turn.name == colaborador["Turno de Trabalho"])
                ).first()
                worker = Workers(
                    name=colaborador["Nome do Colaborador"],
                    function_id=worker_function.id,
                    subsidiarie_id=1,
                    is_active=True,
                    turn_id=worker_turn.id,
                    cost_center_id=1,
                    department_id=1,
                    admission_date="01-01-2025",
                    resignation_date="01-01-2025",
                )
                session.add(worker)
        session.commit()

    # Funções para deleção manual com cascade

    def remove_repeated_turns(all_turns):
        """
        Remove turnos repetidos e deleta, em cascade, os workers associados aos turnos duplicados.
        """
        with Session(engine) as session:
            # Ordena os turnos para facilitar a identificação de duplicatas
            all_turns = sorted(
                all_turns, key=lambda turn: (turn.start_time, turn.end_time)
            )
            previous_turn = None
            for turn in all_turns:
                if (
                    previous_turn
                    and previous_turn.start_time == turn.start_time
                    and previous_turn.end_time == turn.end_time
                ):
                    # Busca e deleta os workers associados ao turno duplicado
                    associated_workers = session.exec(
                        select(Workers).where(Workers.turn_id == turn.id)
                    ).all()
                    for worker in associated_workers:
                        session.delete(worker)
                    session.flush()  # Aplica as deleções dos workers no banco
                    session.delete(turn)
                else:
                    previous_turn = turn
            session.commit()

    def remove_non_operational_functions(all_functions):
        """
        Remove funções não operacionais e deleta, em cascade, os workers associados a essas funções.
        """
        non_operational_ids = [3, 5, 6, 7, 8, 11]
        with Session(engine) as session:
            for function in all_functions:
                if function.id in non_operational_ids or function.name == "Coordenador(a) de Vendas JR":
                    # Busca e deleta os workers associados a esta função
                    associated_workers = session.exec(
                        select(Workers).where(Workers.function_id == function.id)
                    ).all()
                    for worker in associated_workers:
                        session.delete(worker)
                    session.flush()  # Aplica as deleções dos workers
                    session.delete(function)
            session.commit()

    def remove_non_operational_workers(all_workers):
        """
        Remove workers não operacionais.
        """
        non_operational_ids = [3, 5, 6, 7, 8, 11]
        with Session(engine) as session:
            for worker in all_workers:
                if worker.function_id in non_operational_ids or worker.id == 19:
                    session.delete(worker)
            session.commit()

    # Recupera os registros atuais para aplicar as deleções
    with Session(engine) as session:
        all_turns = session.execute(select(Turn)).scalars().all()
        all_functions = session.execute(select(Function)).scalars().all()
        all_workers = session.execute(select(Workers)).scalars().all()

    remove_repeated_turns(all_turns)
    remove_non_operational_functions(all_functions)
    remove_non_operational_workers(all_workers)

    # Remove o arquivo e o diretório temporário
    os.remove(file_location)
    dir_path = os.path.dirname(file_location)
    os.rmdir(dir_path)

    return {
        "all_turns": all_turns,
        "all_functions": all_functions,
        "all_workers": all_workers,
    }
