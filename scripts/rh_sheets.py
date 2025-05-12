import json
from io import BytesIO
from typing import Annotated, Any, Callable, Dict, List, Optional

import pandas as pd
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from sqlmodel import Session, select

from database.sqlite import engine
from models.workers import Workers


class DiscountItem(BaseModel):
    worker: str
    discountNote: str


async def handle_post_scripts_rhsheets(
    discountList: Annotated[str, Form()],
    file: UploadFile = File(...),
):
    try:
        discounts = json.loads(discountList)

        discount_items = [DiscountItem(**item) for item in discounts]

    except (json.JSONDecodeError, ValueError) as e:
        return {"error": f"Formato inválido para discountList: {str(e)}"}

    with Session(engine) as session:
        workers = session.exec(select(Workers)).all()

        worker_esocial_map = {worker.name: worker.esocial for worker in workers}

    contents = await file.read()

    excel_io = BytesIO(contents)

    df = pd.read_excel(excel_io)

    df["descontos"] = ""

    for discount in discount_items:
        mask = df["Nome"].str.lower() == discount.worker.lower()

        if mask.any():
            df.loc[mask, "descontos"] = discount.discountNote

        else:
            print(f"Aviso: Funcionário '{discount.worker}' não encontrado na planilha")

    colunas_desejadas = [
        "Departamento",
        "Nome",
        "Cargo",
        "HE 60%",
        "HE 80%",
        "HE 100%",
        "Folga - DSR",
        "Atestado Médico",
        "FALTA",
        "Folga Gestor",
        "ATRASO",
        "descontos",
    ]

    df_filtrado = df[colunas_desejadas]

    df_filtrado["eSocial"] = df_filtrado["Nome"].map(worker_esocial_map)

    mensagem_atualizacao = "Dados não encontrados - atualize no sistema SGI"

    df_filtrado["eSocial"] = df_filtrado["eSocial"].fillna(mensagem_atualizacao)

    colunas_ordenadas = [
        "Departamento",
        "Nome",
        "eSocial",
        "Cargo",
        "HE 60%",
        "HE 80%",
        "HE 100%",
        "Folga - DSR",
        "Atestado Médico",
        "FALTA",
        "Folga Gestor",
        "ATRASO",
        "descontos",
    ]

    df_filtrado = df_filtrado[colunas_ordenadas]

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for departamento, grupo in df_filtrado.groupby("Departamento"):
            nome_aba = str(departamento)[:31]

            grupo_ordenado = grupo.sort_values(by="Nome")

            nomes_sem_esocial = grupo_ordenado[
                grupo_ordenado["eSocial"] == mensagem_atualizacao
            ]["Nome"].tolist()

            if nomes_sem_esocial:
                print(
                    f"Aviso: Os seguintes funcionários não possuem eSocial cadastrado: {', '.join(nomes_sem_esocial)}"
                )

            grupo_ordenado.to_excel(writer, sheet_name=nome_aba, index=False)

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=departamentos.xlsx"},
    )
