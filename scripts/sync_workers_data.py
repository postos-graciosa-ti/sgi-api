import math
from io import BytesIO

import numpy as np
import pandas as pd
from fastapi import File, UploadFile
from sqlalchemy import and_
from sqlmodel import Session, select

from database.sqlite import engine
from models.workers import Workers


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


def convert_value(value):
    if isinstance(value, pd.Timestamp):
        return value.to_pydatetime()

    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None

    return value


async def handle_post_sync_workers_data(
    subsidiarie_id: int, file: UploadFile = File(...)
):
    with Session(engine) as session:
        contents = await file.read()

        excel_io = BytesIO(contents)

        df = pd.read_excel(excel_io)

        df = df.replace([np.inf, -np.inf], np.nan)

        df = df.where(pd.notnull(df), None)

        data = df.to_dict(orient="records")

        cleaned_data = clean_nans(data)

        field_map = {
            "cpf": "cpf",
            "Carteira de Trabalho": "ctps",
            "Data de Nascimento": "birthdate",
            "email": "email",
            "esocial": "esocial",
            "nome": "name",
            "pis": "pis",
            "rg": "rg",
            "telefone": "mobile",
            "ponto": "timecode",
        }

        updated_workers = []

        for worker in cleaned_data:
            nome = worker.get("nome")

            if not nome:
                continue

            in_db_worker = session.exec(
                select(Workers).where(
                    and_(Workers.name == nome, Workers.subsidiarie_id == subsidiarie_id)
                )
            ).first()

            if in_db_worker:
                for excel_field, model_field in field_map.items():
                    if not model_field or excel_field not in worker:
                        continue

                    value = worker[excel_field]

                    if value not in [None, ""]:
                        setattr(in_db_worker, model_field, convert_value(value))

                session.add(in_db_worker)

                updated_workers.append(in_db_worker)

        session.commit()

        all_workers = session.exec(select(Workers)).all()

        return {
            "updated": len(updated_workers),
            # "workers": updated_workers,
            "all_workers": all_workers,
        }
