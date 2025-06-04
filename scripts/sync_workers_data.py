import math
import re
from datetime import datetime
from io import BytesIO

import numpy as np
import pandas as pd
from fastapi import File, UploadFile
from sqlmodel import Session, select
from unidecode import unidecode

from database.sqlite import engine
from models.workers import Workers


async def handle_post_sync_workers_data(file: UploadFile = File(...)):
    def clean_nans(obj):
        if isinstance(obj, float):
            if math.isnan(obj) or math.isinf(obj):
                return None

            return obj

        elif isinstance(obj, dict):
            return {k: clean_nans(v) for k, v in obj.items()}

        elif isinstance(obj, list):
            return [clean_nans(v) for v in obj]

        return obj

    def convert_to_date(value):
        if value is None:
            return None

        if isinstance(value, pd.Timestamp):
            return value.to_pydatetime().date()

        if isinstance(value, datetime.datetime):
            return value.date()

        return value

    def normalize_name(name):
        if not name:
            return ""

        return re.sub(r"\s+", " ", unidecode(name.strip().lower()))

    contents = await file.read()

    file_extension = file.filename.lower().split(".")[-1]

    if file_extension == "csv":
        df = pd.read_csv(BytesIO(contents), encoding_errors="ignore")

    elif file_extension in ["xlsx", "xls"]:
        engine_used = "openpyxl" if file_extension == "xlsx" else "xlrd"

        df = pd.read_excel(BytesIO(contents), engine=engine_used)

    else:
        return {"error": "Unsupported file format. Please upload a CSV or Excel file."}

    df.columns = df.columns.str.strip().str.lower()

    df = df.replace([np.inf, -np.inf], np.nan)

    df = df.where(pd.notnull(df), None)

    if "nome" not in df.columns:
        return {"error": "A coluna 'nome' é obrigatória no arquivo."}

    df = df[df["nome"].notnull() & df["nome"].str.strip().astype(bool)]

    data = df.to_dict(orient="records")

    cleaned_data = clean_nans(data)

    updated_workers = []

    not_found_names = []

    with Session(engine) as session:
        all_workers = session.exec(select(Workers)).all()

        normalized_workers = {
            normalize_name(worker.name): worker for worker in all_workers
        }

        for entry in cleaned_data:
            nome = entry.get("nome", "")

            if not nome or not nome.strip():
                continue

            normalized_name = normalize_name(nome)

            worker_in_db = normalized_workers.get(normalized_name)

            if not worker_in_db:
                not_found_names.append(nome)

                continue

            if "rg" in entry:
                worker_in_db.rg = entry["rg"]

            if "ctps" in entry:
                worker_in_db.ctps = entry["ctps"]

            if "pis" in entry:
                worker_in_db.pis = entry["pis"]

            if "cpf" in entry:
                worker_in_db.cpf = entry["cpf"]

            if "data de nascimento" in entry:
                worker_in_db.birthdate = convert_to_date(entry["data de nascimento"])

            if "admissão" in entry:
                worker_in_db.admission_date = convert_to_date(entry["admissão"])

            if "esocial" in entry:
                worker_in_db.esocial = entry["esocial"]

            session.add(worker_in_db)

            updated_workers.append(worker_in_db)

        session.commit()

    return {
        "updated_workers": len(updated_workers),
        "not_found_names": not_found_names,
    }
