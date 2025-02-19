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

        with Session(engine) as session:
            new_workers = []

            refactor_tomorrow = Turn(
                name="06:00 - 15:00",
                start_time=time(6, 0),
                end_time=time(15, 0),
                start_interval_time=time(),
                end_interval_time=time(),
                subsidiarie_id=id   
            )

            session.add(refactor_tomorrow)

            session.commit()

            session.refresh(refactor_tomorrow)

            for worker in workers_list:
                functions_options = session.exec(select(Function).where(Function.subsidiarie_id == id)).all()

                turns_options = session.exec(select(Turn).where(Turn.subsidiarie_id == id)).all()

                exist_worker = session.exec(select(Workers).where(Workers.subsidiarie_id == id).where(Workers.name == worker["Nome do Colaborador"])).first()

                if not exist_worker:
                    new_worker_function_id = next((option.id for option in functions_options if option.name == worker["Cargo Atual"]), None)

                    new_worker_turn_id = next((option.id for option in turns_options if option.name == worker["Turno de Trabalho"]),None)

                    if worker["Turno de Trabalho"] == "14:00-22:00":
                        new_worker_turn_id = next((option.id for option in turns_options if option.name == "14:00 - 22:00"), None)

                    neo = Workers(
                        name=worker["Nome do Colaborador"],
                        function_id=new_worker_function_id,
                        subsidiarie_id=id,
                        is_active=True,
                        turn_id=new_worker_turn_id,
                        cost_center_id=1,
                        department_id=1,
                        admission_date=date(2025, 1, 1),
                        resignation_date=date(2025, 1, 1)
                    )
                    
                    new_workers.append(neo)

            if new_workers:
                session.add_all(new_workers)
            
                session.commit()

        all_subsidiarie_functions = session.exec(select(Function).where(Function.subsidiarie_id == id)).all()

        all_subsidiarie_turns = session.exec(select(Turn).where(Turn.subsidiarie_id == id)).all()

        all_subsidiarie_workers = session.exec(select(Workers).where(Workers.subsidiarie_id == id)).all()
        
        return {
            "all_subsidiarie_functions": all_subsidiarie_functions,
            "all_subsidiarie_turns": all_subsidiarie_turns,
            "all_subsidiarie_workers": all_subsidiarie_workers
        }
