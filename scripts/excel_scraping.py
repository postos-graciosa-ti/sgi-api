import os
import re
from datetime import date, datetime, time
from pathlib import Path

import pandas as pd
from fastapi import File, UploadFile
from sqlmodel import Session, select

from database.sqlite import engine
from models.cost_center import CostCenter  # Modelo de CostCenter
from models.department import Department  # Modelo de Department
from models.function import Function
from models.turn import Turn
from models.workers import Workers
from datetime import datetime, timedelta


async def save_uploaded_file(file: UploadFile, upload_dir: str) -> Path:
    Path(upload_dir).mkdir(parents=True, exist_ok=True)

    file_location = Path(upload_dir) / file.filename

    with open(file_location, "wb") as f:
        content = await file.read()

        f.write(content)

    return file_location


def clean_up_file(file_location: Path):
    os.remove(file_location)

    dir_path = os.path.dirname(file_location)

    os.rmdir(dir_path)


def get_unit_name(id: int) -> str:
    units_mapping = {
        1: "Posto Graciosa (1º)",
        2: "Posto Fatima (2º)",
        3: "Posto Bemer (3º)",
        4: "Posto Jariva (4º)",
        5: "Posto Graciosa V (5º)",
        6: "Posto Pirai (6º)",
    }

    return units_mapping if id == 0 else {id: units_mapping.get(id)}


def extract_workers_from_excel(file_location: Path, units: dict):
    df = pd.read_excel(file_location)

    # Filtrando apenas as linhas ativas e as unidades desejadas
    filtered_df = df[df["Unidade"].isin(units.values()) & (df["Status(F)"] == "Ativo")]

    # Ajustando os nomes das colunas para corresponder à sua planilha
    workers_columns = filtered_df[
        [
            "Nome do Colaborador",
            "Cargo Atual",
            "Turno de Trabalho",
            "Unidade",
            "C.Custo",
            "Setor",
            "Admissão",
        ]
    ]

    return workers_columns.where(pd.notna(workers_columns), None).to_dict(
        orient="records"
    )


def get_or_create_function(session: Session, function_name: str, subsidiarie_id: int):
    function = session.exec(
        select(Function).where(
            Function.name == function_name, Function.subsidiarie_id == subsidiarie_id
        )
    ).first()

    if not function:
        function = Function(
            name=function_name, description=function_name, subsidiarie_id=subsidiarie_id
        )

        session.add(function)

        session.commit()

        session.refresh(function)

    return function


def parse_turn(turn_str: str):
    regex = r"^(.*)-(.*)$"

    match = re.match(regex, turn_str)

    if match:
        return (
            datetime.strptime(match.group(1).strip(), "%H:%M").time(),
            datetime.strptime(match.group(2).strip(), "%H:%M").time(),
        )

    return None, None


def get_or_create_turn(session: Session, turn_str: str, subsidiarie_id: int):
    start_time, end_time = parse_turn(turn_str)

    if not start_time or not end_time:
        return None

    turn = session.exec(
        select(Turn).where(
            Turn.start_time == start_time,
            Turn.end_time == end_time,
            Turn.subsidiarie_id == subsidiarie_id,
        )
    ).first()

    if not turn:
        turn = Turn(
            name=turn_str,
            start_time=start_time,
            end_time=end_time,
            start_interval_time=time(0, 0),
            end_interval_time=time(0, 0),
            subsidiarie_id=subsidiarie_id,
        )

        session.add(turn)

        session.commit()

        session.refresh(turn)

    return turn


def get_or_create_cost_center(
    session: Session, cost_center_name: str, subsidiarie_id: int
):
    cost_center = session.exec(
        select(CostCenter).where(CostCenter.name == cost_center_name)
    ).first()

    if not cost_center:
        cost_center = CostCenter(name=cost_center_name, description=cost_center_name)

        session.add(cost_center)

        session.commit()

        session.refresh(cost_center)

    return cost_center


def get_or_create_department(
    session: Session, department_name: str, subsidiarie_id: int
):
    department = session.exec(
        select(Department).where(Department.name == department_name)
    ).first()

    if not department:
        department = Department(name=department_name, description=department_name)

        session.add(department)

        session.commit()

        session.refresh(department)

    return department


def get_or_create_worker(
    session: Session,
    worker: dict,
    function_id: int,
    turn_id: int,
    cost_center_id: int,
    department_id: int,
    subsidiarie_id: int,
):
    existing_worker = session.exec(
        select(Workers).where(
            Workers.name == worker["Nome do Colaborador"],
            Workers.subsidiarie_id == subsidiarie_id,
        )
    ).first()

    if not existing_worker:
        admission_date = worker["Admissão"]

        if isinstance(admission_date, pd.Timestamp):
            admission_date = admission_date.date()

        first_review_date = (admission_date + timedelta(days=30)).strftime("%Y-%m-%d")

        second_review_date = (admission_date + timedelta(days=60)).strftime("%Y-%m-%d")

        new_worker = Workers(
            name=worker["Nome do Colaborador"],
            function_id=function_id,
            subsidiarie_id=subsidiarie_id,
            is_active=True,
            turn_id=turn_id,
            cost_center_id=cost_center_id,
            department_id=department_id,
            admission_date=admission_date,
            resignation_date=date(2025, 1, 1),
            first_review_date=first_review_date,
            second_review_date=second_review_date,
        )

        session.add(new_worker)

        session.commit()


def process_workers(session: Session, workers_list: list, units: dict):
    turns_dict = {}

    for worker in workers_list:
        subsidiarie_id = next(k for k, v in units.items() if v == worker["Unidade"])

        function = get_or_create_function(
            session, worker["Cargo Atual"], subsidiarie_id
        )

        turn = get_or_create_turn(session, worker["Turno de Trabalho"], subsidiarie_id)

        cost_center = get_or_create_cost_center(
            session, worker["C.Custo"], subsidiarie_id
        )

        department = get_or_create_department(session, worker["Setor"], subsidiarie_id)

        if turn:
            turns_dict[worker["Turno de Trabalho"].strip().lower()] = turn.id

            get_or_create_worker(
                session,
                worker,
                function.id,
                turn.id,
                cost_center.id,
                department.id,
                subsidiarie_id,
            )


async def handle_excel_scraping(id: int, file: UploadFile = File(...)):
    units = get_unit_name(id)

    if not units:
        return {"status": "error", "message": "Invalid unit ID"}

    file_location = await save_uploaded_file(file, "uploads")

    workers_list = extract_workers_from_excel(file_location, units)

    clean_up_file(file_location)

    with Session(engine) as session:
        process_workers(session, workers_list, units)

    return {"status": "ok"}
