import os
from datetime import time
from pathlib import Path

import pandas as pd
from fastapi import File, UploadFile
from sqlmodel import Session, select

from database.sqlite import engine
from functions.excel import convert_to_time, extract_turn_info
from models.function import Function
from models.turn import Turn
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

    with Session(engine) as session:
        for colaborador in colaboradores_list:
            name = colaborador["Cargo Atual"]

            description = colaborador["Cargo Atual"]

            turn_string = colaborador["Turno de Trabalho"]

            existing_function = session.exec(
                select(Function).where(Function.name == name)
            ).first()

            if not existing_function:
                new_function = Function(name=name, description=description)

                session.add(new_function)

                session.commit()

                function_id = new_function.id
            else:
                function_id = existing_function.id

            (
                start_time_str,
                start_interval_time_str,
                end_time_str,
                end_interval_time_str,
            ) = extract_turn_info(turn_string)

            start_time = convert_to_time(start_time_str)

            end_time = convert_to_time(end_time_str)

            start_interval_time = (
                convert_to_time(start_interval_time_str)
                if start_interval_time_str
                else time(0, 0)
            )

            end_interval_time = (
                convert_to_time(end_interval_time_str)
                if end_interval_time_str
                else time(0, 0)
            )

            existing_turn = session.exec(
                select(Turn).where(
                    Turn.name == name,
                    Turn.start_time == start_time,
                    Turn.end_time == end_time,
                )
            ).first()

            if not existing_turn:
                new_turn = Turn(
                    name=name,
                    start_time=start_time,
                    start_interval_time=start_interval_time,
                    end_time=end_time,
                    end_interval_time=end_interval_time,
                )

                session.add(new_turn)

                session.commit()

            turn_id = existing_turn.id if existing_turn else new_turn.id

            new_worker = Workers(
                name=colaborador["Nome do Colaborador"],
                function_id=function_id,
                subsidiarie_id=1,
                turn_id=turn_id,
            )

            session.add(new_worker)

        session.commit()

    os.remove(file_location)

    dir_path = os.path.dirname(file_location)

    os.rmdir(dir_path)

    return colaboradores_list
