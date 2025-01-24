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

    with open(file_location, "wb") as f:
        f.write(await file.read())

        df = pd.read_excel(file_location)

        colaboradores_posto_graciosa = df[
            (df["Unidade"] == "Posto Graciosa (1º)") & (df["Status(F)"] == "Ativo")
        ]

        colaboradores_nome_email = colaboradores_posto_graciosa[
            ["Nome do Colaborador", "Cargo Atual", "Turno de Trabalho"]
        ]

        colaboradores_nome_email = colaboradores_nome_email.where(
            pd.notna(colaboradores_nome_email), None
        )

        colaboradores_list = colaboradores_nome_email.to_dict(orient="records")

        todos = []

    regex = r"^(.*)-(.*)$"

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
                )
                session.add(function)

            exist_worker = session.exec(
                select(Workers).where(
                    Workers.name == colaborador["Nome do Colaborador"]
                )
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
                )

                session.add(worker)

        session.commit()

    def remove_repeated_turns(all_turns):
        with Session(engine) as session:
            # Ordenar todos os turnos por start_time e end_time para garantir que duplicatas estejam consecutivas
            all_turns = sorted(all_turns, key=lambda turn: (turn.start_time, turn.end_time))
            
            previous_turn = None
            for turn in all_turns:
                if previous_turn and previous_turn.start_time == turn.start_time and previous_turn.end_time == turn.end_time:
                    session.delete(turn)
                else:
                    previous_turn = turn

            session.commit()

    with Session(engine) as session:
        all_turns = session.execute(select(Turn)).scalars().all()
        all_functions = session.execute(select(Function)).scalars().all()
        all_workers = session.execute(select(Workers)).scalars().all()

    remove_repeated_turns(all_turns)

    os.remove(file_location)

    dir_path = os.path.dirname(file_location)

    os.rmdir(dir_path)

    return {
        "all_turns": all_turns,
        "all_functions": all_functions,
        "all_workers": all_workers,
    }
