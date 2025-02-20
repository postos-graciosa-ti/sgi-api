import os
import re
from datetime import date, datetime, time
from pathlib import Path

import pandas as pd
from fastapi import File, UploadFile
from sqlmodel import Session, select

from database.sqlite import engine
from models.function import Function
from models.turn import Turn
from models.workers import Workers


async def handle_excel_scraping(id, file: UploadFile = File(...)):
    units_mapping = {
        1: "Posto Graciosa (1º)",
        2: "Posto Fatima (2º)",
        3: "Posto Bemer (3º)",
        4: "Posto Jariva (4º)",
        5: "Posto Graciosa V (5º)",
        6: "Posto Pirai (6º)",
    }

    unit = units_mapping.get(id)

    UPLOAD_DIR = "uploads"

    Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

    file_location = Path(UPLOAD_DIR) / file.filename

    with open(file_location, "wb") as f:
        content = await file.read()

        f.write(content)

    df = pd.read_excel(file_location)

    subsidiarie_workers = df[(df["Unidade"] == unit) & (df["Status(F)"] == "Ativo")]

    workers_columns = subsidiarie_workers[
        ["Nome do Colaborador", "Cargo Atual", "Turno de Trabalho"]
    ]

    workers_columns = workers_columns.where(pd.notna(workers_columns), None)

    workers_list = workers_columns.to_dict(orient="records")

    os.remove(file_location)

    dir_path = os.path.dirname(file_location)

    os.rmdir(dir_path)

    with Session(engine) as session:
        turns_dict = {}
        
        existing_worker_names = set()

        for worker in workers_list:
            function = session.exec(
                select(Function).where(
                    Function.name == worker["Cargo Atual"],
                    Function.subsidiarie_id == id,
                )
            ).first()

            if not function:
                function = Function(
                    name=worker["Cargo Atual"],
                    description=worker["Cargo Atual"],
                    subsidiarie_id=id,
                )

                session.add(function)
                
                session.commit()
                
                session.refresh(function)

            regex = r"^(.*)-(.*)$"
            
            turn_parts = re.match(regex, worker["Turno de Trabalho"])

            if turn_parts:
                turn_start_time = datetime.strptime(
                    turn_parts.group(1).strip(), "%H:%M"
                ).time()
                
                turn_end_time = datetime.strptime(
                    turn_parts.group(2).strip(), "%H:%M"
                ).time()
            
            else:
                continue

            turn = session.exec(
                select(Turn).where(
                    Turn.start_time == turn_start_time,
                    Turn.end_time == turn_end_time,
                    Turn.subsidiarie_id == id,
                )
            ).first()

            if not turn:
                turn = Turn(
                    name=worker["Turno de Trabalho"],
                    start_time=turn_start_time,
                    end_time=turn_end_time,
                    start_interval_time=time(0, 0),
                    end_interval_time=time(0, 0),
                    subsidiarie_id=id,
                )

                session.add(turn)

                session.commit()
                
                session.refresh(turn)

            turns_dict[worker["Turno de Trabalho"].strip().lower()] = turn.id

            existing_worker = session.exec(
                select(Workers).where(
                    Workers.name == worker["Nome do Colaborador"],
                    Workers.subsidiarie_id == id,
                )
            ).first()

            if not existing_worker:
                new_worker = Workers(
                    name=worker["Nome do Colaborador"],
                    function_id=function.id,
                    subsidiarie_id=id,
                    is_active=True,
                    turn_id=turn.id,
                    cost_center_id=1,
                    department_id=1,
                    admission_date=date(2025, 1, 1),
                    resignation_date=date(2025, 1, 1),
                )
                session.add(new_worker)
                session.commit()

    return {"status": "ok"}
