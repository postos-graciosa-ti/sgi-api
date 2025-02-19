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

    workers_columns = subsidiarie_workers[["Nome do Colaborador", "Cargo Atual", "Turno de Trabalho"]]

    workers_columns = workers_columns.where(pd.notna(workers_columns), None)

    workers_list = workers_columns.to_dict(orient="records")

    os.remove(file_location)

    dir_path = os.path.dirname(file_location)

    os.rmdir(dir_path)

    with Session(engine) as session:
        subsidiarie_functions_query = select(Function).where(Function.subsidiarie_id == id)

        subsidiarie_functions = session.exec(subsidiarie_functions_query).all() or []

        subsidiarie_turns_query = select(Turn).where(Turn.subsidiarie_id == id)

        subsidiarie_turns = session.exec(subsidiarie_turns_query).all() or []

        for worker in workers_list:
            if worker["Cargo Atual"] not in [func.name for func in subsidiarie_functions]:
                function = Function(
                    name=worker["Cargo Atual"],
                    description=worker["Cargo Atual"],
                    subsidiarie_id=id
                )

                subsidiarie_functions.append(function)

            regex = r"^(.*)-(.*)$"

            turn_parts = re.match(regex, worker["Turno de Trabalho"])

            turn_start_time = datetime.strptime(turn_parts.group(1).strip(), "%H:%M").time()

            turn_end_time = datetime.strptime(turn_parts.group(2).strip(), "%H:%M").time()

            turn_start_interval_time = time(0, 0)

            turn_end_interval_time = time(0, 0)

            if turn_start_time not in [turn.start_time for turn in subsidiarie_turns] and turn_end_time not in [turn.end_time for turn in subsidiarie_turns]:
                turn = Turn(
                    name=worker["Turno de Trabalho"],
                    start_time=turn_start_time,
                    end_time=turn_end_time,
                    start_interval_time=turn_start_interval_time,
                    end_interval_time=turn_end_interval_time,
                    subsidiarie_id=id
                )

                subsidiarie_turns.append(turn)

        session.add_all(subsidiarie_functions)

        session.add_all(subsidiarie_turns)

        session.commit()
        
        new_workers = []

        functions_options = session.exec(select(Function).where(Function.subsidiarie_id == id)).all()
        
        turns_options = session.exec(select(Turn).where(Turn.subsidiarie_id == id)).all()

        turns_dict = {option.name.strip().lower(): option.id for option in turns_options}

        subsidiarie_workers_query = select(Workers).where(Workers.subsidiarie_id == id)
        
        subsidiarie_workers = session.exec(subsidiarie_workers_query).all() or []

        existing_worker_names = {db_worker.name.strip().lower() for db_worker in subsidiarie_workers}

        for worker in workers_list:
            if worker["Nome do Colaborador"].strip().lower() not in existing_worker_names:
                worker_turn = worker["Turno de Trabalho"].strip().lower()
                
                exist_turn = turns_dict.get(worker_turn)

                if not exist_turn:
                    turn_parts = re.match(regex, worker["Turno de Trabalho"])

                    if turn_parts:
                        turn_start_time = datetime.strptime(turn_parts.group(1).strip(), "%H:%M").time()

                        turn_end_time = datetime.strptime(turn_parts.group(2).strip(), "%H:%M").time()
                        
                        turn = Turn(
                            name=worker["Turno de Trabalho"],
                            start_time=turn_start_time,
                            end_time=turn_end_time,
                            start_interval_time=time(0, 0),
                            end_interval_time=time(0, 0),
                            subsidiarie_id=id
                        )
                        
                        session.add(turn)

                        session.commit()

                        session.refresh(turn)

                        exist_turn = turn.id

                format_turn_id = turns_dict.get("14:00 - 22:00") if worker_turn == "14:00-22:00" else exist_turn

                function_id = next((option.id for option in functions_options if option.name == worker["Cargo Atual"]), None)

                neo = Workers(
                    name=worker["Nome do Colaborador"],
                    function_id=function_id,
                    subsidiarie_id=id,
                    is_active=True,
                    turn_id=format_turn_id,
                    cost_center_id=1,
                    department_id=1,
                    admission_date=date(2025, 1, 1),
                    resignation_date=date(2025, 1, 1)
                )
                
                new_workers.append(neo)

        if new_workers:
            session.add_all(new_workers)
            
            session.commit()

        return {"status": "ok"}
