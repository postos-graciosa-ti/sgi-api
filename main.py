import base64
import datetime
import io
import json
import logging
import math
import mimetypes
import os
import re
import smtplib
import subprocess
import tempfile
import threading
import time
from collections import defaultdict
from datetime import date, datetime, timedelta
from email.message import EmailMessage
from functools import wraps
from io import BytesIO
from typing import Annotated, Any, Callable, Dict, List, Optional, Set

import httpx
import numpy as np
import pandas as pd
import pdfplumber
import PyPDF2
import requests
from cachetools import TTLCache
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from fastapi import (
    APIRouter,
    Body,
    Depends,
    FastAPI,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
    status,
)
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from openpyxl import Workbook, load_workbook
from passlib.hash import pbkdf2_sha256
from pydantic import BaseModel, EmailStr
from PyPDF2 import PdfReader, PdfWriter
from sqlalchemy import (
    and_,
    create_engine,
    desc,
    event,
    extract,
    func,
    inspect,
    or_,
    text,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlmodel import Column, Field, LargeBinary, Session, SQLModel, select
from starlette.status import HTTP_404_NOT_FOUND
from unidecode import unidecode

from controllers.all_subsidiaries_no_review import (
    handle_get_away_return_workers,
    handle_get_workers_without_first_review_in_range_all,
    handle_get_workers_without_second_review_in_range_all,
)
from controllers.cnh_categories import handle_get_cnh_categories
from controllers.hierarchy_structure import handle_get_hierarchy_structure
from controllers.root import (
    handle_on_startup,
)
from controllers.wage_payment_method import handle_get_wage_payment_method
from controllers.workers_parents import (
    handle_delete_workers_parents,
    handle_get_workers_parents,
    handle_post_workers_parents,
)
from database.sqlite import engine
from functions.auth import verify_token
from keep_alive import keep_alive_function
from middlewares.cors_middleware import add_cors_middleware
from models.applicants import Applicants
from models.civil_status import CivilStatus
from models.ethnicity import Ethnicity
from models.function import Function
from models.genders import Genders
from models.nationalities import Nationalities
from models.neighborhoods import Neighborhoods
from models.scale import Scale
from models.school_levels import SchoolLevels
from models.service import Service
from models.states import States
from models.subsidiarie import Subsidiarie
from models.tickets import Tickets
from models.tickets_comments import TicketsComments
from models.turn import Turn
from models.user import User
from models.workers import Workers
from models.workers_courses import WorkersCourses
from models.workers_parents import WorkersParents
from models.workers_periodic_reviews import WorkersPeriodicReviews
from private_routes import private_routes
from public_routes import public_routes
from pyhints.no_reviews import SubsidiaryFilter

load_dotenv()

app = FastAPI()

add_cors_middleware(app)


@app.on_event("startup")
def on_startup():
    threading.Thread(target=keep_alive_function, daemon=True).start()

    handle_on_startup()


# include public routes

for public_route in public_routes:
    app.include_router(public_route)

# include private routes

for private_route in private_routes:
    app.include_router(private_route)


@app.get("/workerscourses/current-month")
def get_courses_current_month():
    now = datetime.now()
    start_month = datetime(now.year, now.month, 1)

    if now.month == 12:
        next_month = datetime(now.year + 1, 1, 1)
    else:
        next_month = datetime(now.year, now.month + 1, 1)

    with Session(engine) as session:
        # Busca todos os cursos (sem filtro de data no SQL)
        statement = select(WorkersCourses).order_by(desc(WorkersCourses.id))
        courses = session.exec(statement).all()

        result = []

        for c in courses:
            try:
                # Converte a string para datetime
                date_obj = datetime.fromisoformat(c.date_file)
            except Exception:
                # Ignora registros com formato inválido
                continue

            # Filtra cursos dentro do mês atual
            if start_month <= date_obj < next_month:
                worker = session.get(Workers, c.worker_id)
                worker_name = worker.name if worker else "Desconhecido"

                result.append(
                    {
                        "id": c.id,
                        "worker_id": c.worker_id,
                        "worker_name": worker_name,
                        "date_file": c.date_file,
                        "is_payed": c.is_payed,
                    }
                )

        return result


@app.get("/workers-courses/file/{course_id}")
def get_course_file(course_id: int):
    with Session(engine) as session:
        course = session.get(WorkersCourses, course_id)

        if not course:
            raise HTTPException(status_code=404, detail="Curso não encontrado")

        file_like = io.BytesIO(course.file)

        return StreamingResponse(
            file_like,
            media_type="application/pdf",
            headers={"Content-Disposition": f"inline; filename=curso_{course_id}.pdf"},
        )


@app.post("/workers-courses")
async def create_worker_course(
    worker_id: int = Form(...),
    date_file: str = Form(...),
    is_payed: str = Form(...),
    file: UploadFile = File(...),
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="O arquivo deve ser um PDF.")

    file_data = await file.read()

    try:
        parsed_date = datetime.strptime(date_file, "%Y-%m-%d")

    except ValueError:
        raise HTTPException(
            status_code=400, detail="Data inválida. Use o formato YYYY-MM-DD."
        )

    is_payed_bool = is_payed.lower() == "true"

    new_course = WorkersCourses(
        worker_id=worker_id,
        file=file_data,
        date_file=parsed_date,
        is_payed=is_payed_bool,
    )

    try:
        with Session(engine) as session:
            session.add(new_course)

            session.commit()

            session.refresh(new_course)

    except Exception as e:
        print(e)

        raise HTTPException(status_code=500, detail="Erro ao salvar no banco de dados.")

    return {"id": new_course.id, "message": "Curso cadastrado com sucesso."}


@app.get("/workers-status", dependencies=[Depends(verify_token)])
def get_workers_status():
    with Session(engine) as session:
        subsidiaries = session.exec(select(Subsidiarie)).all()

        functions = session.exec(select(Function)).all()

        turns = session.exec(select(Turn)).all()

        workers = session.exec(
            select(Workers)
            .where(Workers.is_active == True)  # noqa: E712
            .where(Workers.is_away == False)  # noqa: E712
        ).all()

        func_map = {f.id: f.name for f in functions}

        turn_map = {t.id: t.name for t in turns}

        sub_map = {s.id: s.name for s in subsidiaries}

        grouped = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

        count_by_sub = defaultdict(int)

        total_count = 0

        for worker in workers:
            if worker.subsidiarie_id and worker.function_id and worker.turn_id:
                sub_name = sub_map.get(worker.subsidiarie_id, "Desconhecida")

                turn_name = turn_map.get(worker.turn_id, "Sem Turno")

                func_name = func_map.get(worker.function_id, "Sem Função")

                grouped[sub_name][turn_name][func_name].append(worker.name)

                count_by_sub[sub_name] += 1

                total_count += 1

        result = {
            "total_geral": total_count,
            "por_subsidiaria": [],
        }

        for sub_name, turns in grouped.items():
            sub_entry = {
                "subsidiaria": sub_name,
                "total": count_by_sub[sub_name],
                "turnos": [],
            }

            for turn_name, funcs in turns.items():
                turn_entry = {"turno": turn_name, "funções": []}

                for func_name, names in funcs.items():
                    turn_entry["funções"].append(
                        {"função": func_name, "funcionários": names}
                    )

                sub_entry["turnos"].append(turn_entry)

            result["por_subsidiaria"].append(sub_entry)

        return result


@app.post("/workers/{worker_id}/autorize-app", dependencies=[Depends(verify_token)])
def post_workers_autorize_app(worker_id: int):
    with Session(engine) as session:
        db_worker = session.get(Workers, worker_id)

        db_worker.app_login = db_worker.cpf

        db_worker.app_password = pbkdf2_sha256.hash(db_worker.cpf)

        session.add(db_worker)

        session.commit()

        session.refresh(db_worker)

        return {"success": True}


# workers parents


@app.get("/workers/{id}/parents")
def get_workers_parents(id: int):
    return handle_get_workers_parents(id)


@app.post("/workers-parents")
def post_workers_parents(worker_parent: WorkersParents):
    return handle_post_workers_parents(worker_parent)


@app.delete("/workers-parents/{id}")
def delete_workers_parents(id: int):
    return handle_delete_workers_parents(id)


# hierarchy structure


@app.get("/hierarchy-structure")
def get_hierarchy_structure():
    return handle_get_hierarchy_structure()


# wage payment method


@app.get("/wage-payment-methods")
def get_wage_payment_method():
    return handle_get_wage_payment_method()


# hollidays scale


# @app.get("/subsidiaries/{id}/hollidays-scale/{date}")
# def get_hollidays_scale(id: int, date: str):
#     return handle_get_hollidays_scale(id, date)


# @app.post("/hollidays-scale")
# def post_hollidays_scale(holliday_scale: HollidaysScale):
#     return handle_post_hollidays_scale(holliday_scale)


# @app.delete("/hollidays-scale/{id}")
# def delete_hollidays_scale(id: int):
#     return handle_delete_hollidays_scale(id)


# cnh categories


@app.get("/cnh-categories")
def get_cnh_categories():
    return handle_get_cnh_categories()


# @app.delete("/workers/{id}")
# def delete_workers(id: int):
#     with Session(engine) as session:
#         worker = session.exec(select(Workers).where(Workers.id == id)).first()

#         session.delete(worker)

#         session.commit()

#         return {"success": True}


@app.get("/functions/{id}")
def get_function_by_id(id: int):
    with Session(engine) as session:
        function = session.exec(select(Function).where(Function.id == id)).first()

        return function


# all subsidiaries no first review and second review


@app.post("/subsidiaries/workers/experience-time-no-first-review")
async def get_workers_without_first_review_in_range_all(data: SubsidiaryFilter):
    return await handle_get_workers_without_first_review_in_range_all(data)


@app.post("/subsidiaries/workers/experience-time-no-second-review")
async def get_workers_without_second_review_in_range_all(data: SubsidiaryFilter):
    return await handle_get_workers_without_second_review_in_range_all(data)


@app.post("/subsidiaries/away-workers")
def get_away_return_workers(data: SubsidiaryFilter):
    return handle_get_away_return_workers(data)


class ScalesListProps(BaseModel):
    start_date: str
    end_date: str
    turn_id: int | None = None
    function_id: int | None = None


@app.post("/subsidiaries/{id}/scales/list")
def get_scales(id: int, scales_list_props: ScalesListProps):
    with Session(engine) as session:
        start_date = datetime.strptime(scales_list_props.start_date, "%d-%m-%Y").date()

        end_date = datetime.strptime(scales_list_props.end_date, "%d-%m-%Y").date()

        query = select(Scale).where(Scale.subsidiarie_id == id)

        if scales_list_props.turn_id is not None:
            query = query.where(Scale.worker_turn_id == scales_list_props.turn_id)

        if scales_list_props.function_id is not None:
            query = query.where(
                Scale.worker_function_id == scales_list_props.function_id
            )

        scales = session.exec(query).all()

        in_range_scales = []

        for scale in scales:
            worker = session.get(Workers, scale.worker_id)

            scale_days_off = (
                json.loads(scale.days_off)
                if isinstance(scale.days_off, str)
                else scale.days_off or []
            )

            scale_days_on = (
                json.loads(scale.days_on)
                if isinstance(scale.days_on, str)
                else scale.days_on or []
            )

            scale_proportion = (
                json.loads(scale.proportion)
                if isinstance(scale.proportion, str)
                else scale.proportion or []
            )

            valid_days_off = [
                datetime.strptime(day["date"], "%d-%m-%Y").date()
                for day in scale_days_off
                if isinstance(day, dict)
                and "date" in day
                and start_date
                <= datetime.strptime(day["date"], "%d-%m-%Y").date()
                <= end_date
            ]

            valid_days_on = [
                datetime.strptime(day["date"], "%d-%m-%Y").date()
                for day in scale_days_on
                if isinstance(day, dict)
                and "date" in day
                and start_date
                <= datetime.strptime(day["date"], "%d-%m-%Y").date()
                <= end_date
            ]

            valid_proportion = [
                day
                for day in scale_proportion
                if isinstance(day, dict)
                and start_date
                <= datetime.strptime(day["data"], "%d-%m-%Y").date()
                <= end_date
            ]

            in_range_scales.append(
                {
                    "worker": worker,
                    "worker_turn": session.get(Turn, worker.turn_id),
                    "worker_function": session.get(Function, worker.function_id),
                    "days_on": valid_days_on,
                    "days_off": valid_days_off,
                    "proportion": valid_proportion,
                    "start_date": start_date,
                    "end_date": end_date,
                }
            )

        return in_range_scales


# workers docs


class WorkersDocs(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    worker_id: int = Field(foreign_key="workers.id")
    doc: bytes = Field(sa_column=Column(LargeBinary))
    doc_title: str = Field(max_length=100)


@app.get("/worker-pdfs/{worker_id}")
def get_worker_pdfs(worker_id: int):
    try:
        with Session(engine) as session:
            statement = select(WorkersDocs).where(WorkersDocs.worker_id == worker_id)
            docs = session.exec(statement).all()

            if not docs:
                return []

            return [
                {
                    "doc_id": doc.id,
                    "worker_id": doc.worker_id,
                    "size": len(doc.doc),
                    "doc_title": doc.doc_title,
                }
                for doc in docs
            ]

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao buscar documentos: {str(e)}"
        )


# Baixar documento por ID
@app.get("/get-pdf/{doc_id}")
def get_pdf(doc_id: int):
    try:
        with Session(engine) as session:
            doc = session.get(WorkersDocs, doc_id)

            if not doc:
                raise HTTPException(status_code=404, detail="Documento não encontrado")

            if doc.doc_title == "Ficha da contabilidade":
                # Detectar se é .xlsx (formato zip) ou .xls (binário)
                ext = ".xlsx" if doc.doc[:4] == b"PK\x03\x04" else ".xls"
                media_type = (
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    if ext == ".xlsx"
                    else "application/vnd.ms-excel"
                )
                filename = f"ficha_contabilidade_{doc_id}{ext}"
            else:
                media_type = "application/pdf"
                filename = f"document_{doc_id}.pdf"

            return StreamingResponse(
                BytesIO(doc.doc),
                media_type=media_type,
                headers={"Content-Disposition": f"inline; filename={filename}"},
            )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao recuperar documento: {str(e)}"
        )


@app.post("/upload-pdf/{worker_id}")
async def upload_pdf(
    worker_id: int,
    doc_title: str = Form(...),
    file: UploadFile = File(...),
):
    try:
        file_bytes = await file.read()

        if doc_title == "Ficha da contabilidade":
            if file.content_type not in [
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "application/vnd.ms-excel",
            ]:
                raise HTTPException(
                    status_code=400,
                    detail="O arquivo deve estar no formato Excel (.xls ou .xlsx)",
                )

        else:
            if file.content_type != "application/pdf":
                raise HTTPException(
                    status_code=400,
                    detail="O arquivo deve ser um PDF",
                )

        with Session(engine) as session:
            db_doc = WorkersDocs(
                worker_id=worker_id,
                doc=file_bytes,
                doc_title=doc_title,
            )

            session.add(db_doc)

            session.commit()

            session.refresh(db_doc)

            if doc_title == "Contrato de trabalho":
                with pdfplumber.open(BytesIO(file_bytes)) as pdf:
                    if len(pdf.pages) < 10:
                        raise HTTPException(
                            status_code=400,
                            detail="O PDF não possui 10 páginas.",
                        )

                    page = pdf.pages[9]

                    text = page.extract_text()

                    nome = re.search(
                        r"Nome:\s*(.*?)\s*(?=Código:|Pai:|Mãe:|Nascimento:)", text
                    )

                    pai = re.search(r"Pai:\s*(.*?)\s*(?=Nr\.)", text)

                    mae = re.search(r"Mãe:\s*(.*)", text)

                    nascimento = re.search(r"Nascimento:\s*(\d{2}/\d{2}/\d{4})", text)

                    sexo = re.search(r"Sexo:\s*(\w+)", text)

                    estado_civil = re.search(r"Est\.? Civil:\s*(\w+)", text)

                    raca = re.search(r"Ra[çc]a\s*/\s*Cor\s*:\s*(.+?)(?=\n|$)", text)

                    nacionalidade = re.search(r"Nacionalidade:\s*(.+?)(?=\n|$)", text)

                    enderecos = re.findall(
                        r"Endere[cç]o:\s*(.*?)\s*(?=Bairro:|CEP:|Munic[ií]pio:)", text
                    )

                    bairros = re.findall(
                        r"Bairro:\s*(.*?)\s*(?=CEP:|Munic[ií]pio:|Endere[cç]o:)", text
                    )

                    # municipio = re.search(r"Município:\s*(.*)", text)

                    cep = re.search(r"CEP:\s*([\d\.-]+)", text)

                    cpf = re.search(r"CPF:\s*([\d\.-]+)", text)

                    rg = re.search(r"RG:\s*(\S+)", text)

                    # orgao = re.search(r"Órgão:\s*(.+?)(?=\s*Estado:|\n|$)", text)

                    ctps_numero = re.search(r"Número CTPS:\s*(\d+)", text)

                    ctps_serie = re.search(r"Série CTPS:\s*(\d+)", text)

                    ctps_estado = re.search(r"Estado CTPS:\s*([A-Z]{2})", text)

                    pis = re.search(r"PIS:\s*([\d\.\-]+)", text)

                    instrucao = re.search(r"Instru[cç][aã]o:\s*(.+?)(?=\n|$)", text)

                    banco = re.search(r"Banco:\s*(.*)", text)

                    conta = re.search(r"Conta:\s*(\d+)", text)

                    agencia = re.search(r"Agência:\s*(\d+)", text)

                    db_worker = session.get(Workers, worker_id)

                    if db_worker:
                        if nome:
                            db_worker.name = nome.group(1).strip()

                        if pai:
                            db_worker.fathername = pai.group(1).strip()

                        if mae:
                            db_worker.mothername = mae.group(1).strip()

                        if nascimento:
                            try:
                                nascimento_formatada = datetime.strptime(
                                    nascimento.group(1), "%d/%m/%Y"
                                ).strftime("%Y-%m-%d")

                                db_worker.birthdate = nascimento_formatada

                            except ValueError:
                                raise HTTPException(
                                    status_code=400,
                                    detail="Data de nascimento inválida",
                                )

                        if sexo:
                            sexo_nome = sexo.group(1).strip().lower()

                            sexo_db = session.exec(
                                select(Genders).where(
                                    Genders.name.ilike(f"%{sexo_nome}%")
                                )
                            ).first()

                            if sexo_db:
                                db_worker.gender_id = sexo_db.id

                            if estado_civil:
                                estado_nome = estado_civil.group(1).strip().lower()

                                estado_db = session.exec(
                                    select(CivilStatus).where(
                                        CivilStatus.name.ilike(f"%{estado_nome}%")
                                    )
                                ).first()

                                if estado_db:
                                    db_worker.civil_status_id = estado_db.id

                                if raca:
                                    raca_nome = raca.group(1).strip().lower()

                                    feminino_para_masculino = {
                                        "branca": "branco",
                                        "preta": "preto",
                                        "parda": "pardo",
                                        "amarela": "amarelo",
                                        "indígena": "indígena",
                                    }

                                    raca_normalizada = feminino_para_masculino.get(
                                        raca_nome, raca_nome
                                    )

                                    raca_db = session.exec(
                                        select(Ethnicity).where(
                                            Ethnicity.name.ilike(
                                                f"%{raca_normalizada}%"
                                            )
                                        )
                                    ).first()

                                    if raca_db:
                                        db_worker.ethnicity_id = raca_db.id

                        if nacionalidade:
                            nacionalidade_nome = nacionalidade.group(1).strip().lower()

                            nacionalidade_db = session.exec(
                                select(Nationalities).where(
                                    Nationalities.name.ilike(f"%{nacionalidade_nome}%")
                                )
                            ).first()

                            if nacionalidade_db:
                                db_worker.nationality = nacionalidade_db.id

                        if enderecos:
                            endereco_final = enderecos[
                                -1
                            ].strip()  # pega o último endereço encontrado
                            db_worker.street = endereco_final

                        if bairros:
                            bairro_nome = bairros[-1].strip()

                            bairro_db = session.exec(
                                select(Neighborhoods).where(
                                    Neighborhoods.name.ilike(f"%{bairro_nome}%")
                                )
                            ).first()

                            if bairro_db:
                                db_worker.neighborhood_id = bairro_db.id

                        # if municipio:
                        #     db_worker.city = 1

                        if cep:
                            db_worker.cep = cep.group(1).strip()

                        if cpf:
                            db_worker.cpf = cpf.group(1).strip()

                        if rg:
                            db_worker.rg = rg.group(1).strip()

                        # if orgao:
                        #     db_worker.rg_issuing_agency = orgao.group(1).strip()

                        if ctps_numero:
                            db_worker.ctps = ctps_numero.group(1).strip()

                        if ctps_serie:
                            db_worker.ctps_serie = ctps_serie.group(1).strip()

                        if ctps_estado:
                            uf = ctps_estado.group(1).strip().upper()

                            estado_db = session.exec(
                                select(States).where(States.sail == uf)
                            ).first()

                            if estado_db:
                                db_worker.ctps_state = estado_db.id

                        if pis:
                            db_worker.pis = pis.group(1).strip()

                        if instrucao:
                            instrucao_nome = instrucao.group(1).strip().lower()

                            instrucao_db = session.exec(
                                select(SchoolLevels).where(
                                    SchoolLevels.name.ilike(f"%{instrucao_nome}%")
                                )
                            ).first()

                            if instrucao_db:
                                db_worker.school_level = instrucao_db.id

                        if banco:
                            db_worker.bank = 1

                        if conta:
                            db_worker.bank_account = conta.group(1).strip()

                        if agencia:
                            db_worker.bank_agency = agencia.group(1).strip()

                        session.add(db_worker)

                        session.commit()

                EMAIL_REMETENTE = os.environ.get("EMAIL_REMETENTE")

                SENHA = os.environ.get("SENHA")

                BCC = os.environ.get("BCC")

                msg = EmailMessage()

                msg["Subject"] = "Novo contrato de trabalho"

                msg["From"] = EMAIL_REMETENTE

                msg["To"] = BCC

                msg.set_content(
                    "Um novo contrato de trabalho foi anexado ao SGI, confira já!"
                )

                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    smtp.login(EMAIL_REMETENTE, SENHA)

                    smtp.send_message(msg)

            return {
                "message": "Arquivo salvo com sucesso",
                "id": db_doc.id,
                "worker_id": db_doc.worker_id,
                "doc_title": db_doc.doc_title,
                "filename": file.filename,
            }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao salvar o arquivo: {str(e)}"
        )


class EmailRequest(BaseModel):
    worker_id: int
    to: EmailStr
    subject: str
    body: str


@app.post("/send-email")
def send_email(request: EmailRequest):
    EMAIL_REMETENTE = os.environ.get("EMAIL_REMETENTE")

    SENHA = os.environ.get("SENHA")

    BCC = os.environ.get("BCC")

    with Session(engine) as session:
        work_contract = session.exec(
            select(WorkersDocs)
            .where(WorkersDocs.worker_id == request.worker_id)
            .where(WorkersDocs.doc_title == "Contrato de trabalho")
        ).first()

        if not work_contract or not work_contract.doc:
            raise HTTPException(status_code=404, detail="Documento não encontrado.")

        try:
            original_pdf = PdfReader(io.BytesIO(work_contract.doc))

            new_pdf_stream = io.BytesIO()

            writer = PdfWriter()

            for page_num in range(2, 9):
                if page_num < len(original_pdf.pages):
                    writer.add_page(original_pdf.pages[page_num])

            writer.write(new_pdf_stream)

            new_pdf_stream.seek(0)

            msg = EmailMessage()

            msg["Subject"] = request.subject

            msg["From"] = EMAIL_REMETENTE

            msg["To"] = request.to

            msg["Bcc"] = BCC

            msg.set_content(request.body)

            msg.add_attachment(
                new_pdf_stream.read(),
                maintype="application",
                subtype="pdf",
                filename="Contrato_paginas_3_a_9.pdf",
            )

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_REMETENTE, SENHA)

                smtp.send_message(msg)

            return {"message": "E-mail enviado com sucesso com as páginas 3 e 9"}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@app.delete("/workers-docs/{id}")
def delete_workers_docs(id: int):
    with Session(engine) as session:
        doc = session.exec(select(WorkersDocs).where(WorkersDocs.id == id)).first()

        session.delete(doc)

        session.commit()

        return {"success": True}


@app.get("/services")
def get_services():
    with Session(engine) as session:
        services = session.exec(select(Service)).all()

        return services


@app.get("/tickets/requesting/{id}", response_model=list[dict])
def get_tickets_requesting(id: int):
    with Session(engine) as session:
        requesting_user = session.get(User, id)

        if not requesting_user:
            raise HTTPException(status_code=404, detail="Requesting user not found")

        tickets = session.exec(
            select(Tickets)
            .where(Tickets.requesting_id == id)
            .order_by(Tickets.id.desc())
        ).all()

        if not tickets:
            return []

        all_responsible_ids = set()

        service_ids = set()

        for ticket in tickets:
            try:
                responsible_ids = json.loads(ticket.responsibles_ids)

            except (json.JSONDecodeError, TypeError):
                responsible_ids = []

            all_responsible_ids.update(responsible_ids)

            if ticket.service:
                service_ids.add(ticket.service)

        responsibles_map = {
            user.id: user
            for user in session.exec(
                select(User).where(User.id.in_(all_responsible_ids))
            ).all()
        }

        services_map = {
            service.id: service
            for service in session.exec(
                select(Service).where(Service.id.in_(service_ids))
            ).all()
        }

        tickets_data = []

        for ticket in tickets:
            try:
                responsible_ids = json.loads(ticket.responsibles_ids)

            except (json.JSONDecodeError, TypeError):
                responsible_ids = []

            responsibles = [
                responsible.dict()
                for responsible_id in responsible_ids
                if (responsible := responsibles_map.get(responsible_id))
            ]

            tickets_data.append(
                {
                    "ticket_id": ticket.id,
                    "requesting": requesting_user.dict(),
                    "responsibles": responsibles,
                    "service": services_map.get(ticket.service),
                    "description": ticket.description,
                    "is_open": ticket.is_open,
                    "opened_at": ticket.opened_at,
                    "closed_at": ticket.closed_at,
                }
            )

        return tickets_data


@app.post("/tickets")
def post_tickets(ticket: Tickets):
    with Session(engine) as session:
        session.add(ticket)

        session.commit()

        session.refresh(ticket)

        return ticket


@app.patch("/tickets/{ticket_id}/close")
def close_ticket(ticket_id: int):
    with Session(engine) as session:
        ticket = session.get(Tickets, ticket_id)

        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        ticket.is_open = False

        ticket.closed_at = date.today()

        session.add(ticket)

        session.commit()

        return {
            "message": "Ticket fechado com sucesso",
            "closed_at": ticket.closed_at,
        }


@app.get("/tickets-comments/{id}")
def get_tickets_comments(id: int):
    with Session(engine) as session:
        ticket_comments = (
            session.exec(
                select(TicketsComments, User)
                .join(User, TicketsComments.comentator_id == User.id)
                .where(TicketsComments.ticket_id == id)
                .order_by(TicketsComments.ticket_id.asc())
            )
            .mappings()
            .all()
        )

        return ticket_comments


@app.post("/tickets-comments")
def post_tickets_comments(ticket_comment: TicketsComments):
    with Session(engine) as session:
        session.add(ticket_comment)

        session.commit()

        session.refresh(ticket_comment)

        return ticket_comment


@app.get("/tickets/responsible/{id}", response_model=list[dict])
def get_tickets_responsible(id: int):
    with Session(engine) as session:
        responsible_user = session.get(User, id)

        if not responsible_user:
            raise HTTPException(status_code=404, detail="Responsible user not found")

        tickets = session.exec(select(Tickets).order_by(Tickets.id.desc())).all()

        filtered_tickets = []

        for t in tickets:
            try:
                responsible_ids = json.loads(t.responsibles_ids)

            except (json.JSONDecodeError, TypeError):
                responsible_ids = []

            if id in responsible_ids:
                filtered_tickets.append((t, responsible_ids))

        if not filtered_tickets:
            return []

        requesting_ids = {t.requesting_id for t, _ in filtered_tickets}

        all_responsible_ids = set()

        service_ids = set()

        for t, responsible_ids in filtered_tickets:
            all_responsible_ids.update(responsible_ids)

            if t.service:
                service_ids.add(t.service)

        users_map = {
            user.id: user
            for user in session.exec(
                select(User).where(User.id.in_(requesting_ids | all_responsible_ids))
            ).all()
        }

        services_map = {
            service.id: service
            for service in session.exec(
                select(Service).where(Service.id.in_(service_ids))
            ).all()
        }

        tickets_data = []

        for t, responsible_ids in filtered_tickets:
            responsibles = [
                responsible.dict()
                for responsible_id in responsible_ids
                if (responsible := users_map.get(responsible_id))
            ]

            tickets_data.append(
                {
                    "ticket_id": t.id,
                    "requesting": users_map.get(t.requesting_id),
                    "responsibles": responsibles,
                    "service": services_map.get(t.service),
                    "description": t.description,
                    "is_open": t.is_open,
                    "opened_at": t.opened_at,
                    "closed_at": t.closed_at,
                }
            )

        return tickets_data


@app.get("/tickets/responsible/{id}/notifications")
def get_tickets_responsible_notifications(id: int):
    with Session(engine) as session:
        today = date.today()

        start_of_week = (today - timedelta(days=today.weekday())).isoformat()

        end_of_week = (
            datetime.fromisoformat(start_of_week) + timedelta(days=6)
        ).isoformat()

        tickets = (
            session.exec(
                select(Tickets, User, Service)
                .join(User, Tickets.requesting_id == User.id)
                .join(Service, Tickets.service == Service.id)
                .where(Tickets.opened_at >= start_of_week)
                .where(Tickets.opened_at <= end_of_week)
                .where(Tickets.responsibles_ids.contains(id))
                .order_by(Tickets.id.desc())
            )
            .mappings()
            .all()
        )

        return tickets


@app.get("/subsidiaries/{id}/metrics")
def get_subsidiarie_metrics(id: int):
    with Session(engine) as session:
        caixas_function = session.exec(
            select(Function)
            .where(Function.subsidiarie_id == id)
            .where(Function.name == "Operador(a) de Caixa I")
        ).first()

        caixas_at_subsidiarie = session.exec(
            select(Workers)
            .where(Workers.subsidiarie_id == id)
            .where(Workers.function_id == caixas_function.id)
        ).all()

        frentistas_function = session.exec(
            select(Function)
            .where(Function.subsidiarie_id == id)
            .where(Function.name == "Frentista I")
        ).first()

        frentistas_at_subsidiarie = session.exec(
            select(Workers)
            .where(Workers.subsidiarie_id == id)
            .where(Workers.function_id == frentistas_function.id)
        ).all()

        caixas_ideal = caixas_function.ideal_quantity or 9

        frentistas_ideal = frentistas_function.ideal_quantity or 18

        return {
            "caixas_quantity": len(caixas_at_subsidiarie),
            "caixas_ideal_quantity": caixas_ideal,
            "has_caixas_ideal_quantity": len(caixas_at_subsidiarie) >= caixas_ideal,
            "frentistas_quantity": len(frentistas_at_subsidiarie),
            "frentistas_ideal_quantity": frentistas_ideal,
            "has_frentistas_ideal_quantity": len(frentistas_at_subsidiarie)
            >= frentistas_ideal,
        }


#


class AdmissionsReportInput(BaseModel):
    first_day: str
    last_day: str


@app.post("/subsidiaries/{id}/workers/admissions-report")
def get_admissions_report(id: int, input: AdmissionsReportInput):
    with Session(engine) as session:
        first_day = datetime.strptime(input.first_day, "%Y-%m-%d")

        last_day = datetime.strptime(input.last_day, "%Y-%m-%d")

        subsidiarie_workers = session.exec(
            select(Workers).where(Workers.subsidiarie_id == id)
        ).all()

        result = []

        for worker in subsidiarie_workers:
            worker_admission_date = datetime.strptime(worker.admission_date, "%Y-%m-%d")

            if worker_admission_date >= first_day and worker_admission_date <= last_day:
                result.append({"id": worker.id, "name": worker.name})

        return result


class ImagePayload(BaseModel):
    image: str


@app.post("/applicants/{id}/api/upload-image")
async def upload_image(id: int, payload: ImagePayload):
    with Session(engine) as session:
        applicant = session.exec(select(Applicants).where(Applicants.id == id)).first()

        if not applicant:
            raise HTTPException(status_code=404, detail="Applicant não encontrado")

        applicant.picture_url = payload.image

        applicant.identity_complete = True

        session.add(applicant)

        session.commit()

        print(f"Imagem salva para applicant {id}: {payload.image}")

        return {"status": "ok"}


class SendEmailToMabeconBodyProps(BaseModel):
    subsidiarie: str
    worker_name: str
    worker_admission_date: str


@app.post("/send-email-to-mabecon")
def post_send_email_to_mabecon(body: SendEmailToMabeconBodyProps):
    EMAIL_REMETENTE = os.environ.get("EMAIL_REMETENTE")

    SENHA = os.environ.get("SENHA")

    MABECON_EMAIL = os.environ.get("MABECON_EMAIL")

    BCC = os.environ.get("BCC")

    msg = EmailMessage()

    msg["Subject"] = f"Solicitação de admissão para {body.worker_name}"

    msg["From"] = EMAIL_REMETENTE

    msg["To"] = MABECON_EMAIL

    msg["Bcc"] = BCC

    msg.set_content(
        f"""
            Prezada Mabecon,

            Solicitamos a admissão de {body.worker_name} para {body.subsidiarie}, com data prevista de ínicio para {body.worker_admission_date},

            Demais informações de funcionário disponíveis em https://sgi-front-prod.onrender.com,

            Desde já, agradecemos o serviço prestado,

            Atenciosamente,

            RH Postos Graciosa
            """
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_REMETENTE, SENHA)

        smtp.send_message(msg)

        return {"message": "E-mail enviado com sucesso"}


@app.post("/users/recovery-password/send-email")
def recovery_user_password_send_email(user: User):
    with Session(engine) as session:
        GMAIL_USER = os.environ.get("EMAIL_REMETENTE")

        GMAIL_APP_PASSWORD = os.environ.get("SENHA")

        db_user = session.exec(
            select(User).where(and_(User.name == user.name, User.email == user.email))
        ).first()

        if not db_user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        msg = EmailMessage()

        msg["Subject"] = "Recuperação de senha"

        msg["From"] = GMAIL_USER

        msg["To"] = db_user.email

        msg.set_content(
            f"""
            Olá {db_user.name},

            Recebemos uma solicitação para redefinir sua senha. 
            Clique no link abaixo para continuar o processo de recuperação:

            https://seusite.com/recovery/{db_user.id}

            Se você não solicitou isso, ignore este e-mail.

            Atenciosamente,
            Equipe de Suporte
            """
        )

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
                smtp.starttls()

                smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)

                smtp.send_message(msg)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao enviar e-mail: {e}")

        return {"message": "E-mail de recuperação enviado com sucesso"}


@app.get("/workers-periodic-reviews/{worker_id}")
def get_workers_periodic_reviews(worker_id: int):
    with Session(engine) as session:
        workers_periodic_reviews = session.exec(
            select(WorkersPeriodicReviews).where(
                WorkersPeriodicReviews.worker_id == worker_id
            )
        ).all()

        result = [
            {
                "id": review.id,
                "worker_id": review.worker_id,
                "label": review.label,
                "date": review.date,
                "answers": json.loads(review.answers),
            }
            for review in workers_periodic_reviews
        ]

        return result


@app.post("/workers-periodic-reviews")
def post_workers_periodic_reviews(body: WorkersPeriodicReviews):
    with Session(engine) as session:
        session.add(body)

        session.commit()

        session.refresh(body)

        return body


@app.delete("/workers-periodic-reviews/{id}")
def delete_workers_periodic_reviews(id: int):
    with Session(engine) as session:
        db_review = session.exec(
            select(WorkersPeriodicReviews).where(WorkersPeriodicReviews.id == id)
        ).first()

        session.delete(db_review)

        session.commit()

        return {"success": True}


class NrBodyProps(BaseModel):
    message: str


@app.post("/send-nr-20-email-to-coordinators")
def post_send_email_to_coordinators(body: NrBodyProps):
    with Session(engine) as session:
        managers = session.exec(select(Subsidiarie.manager)).all()

        coordinators = session.exec(select(Subsidiarie.coordinator)).all()

        staffs = set(managers + coordinators)

        EMAIL_REMETENTE = os.environ.get("EMAIL_REMETENTE")

        SENHA = os.environ.get("SENHA")

        BCC = os.environ.get("BCC")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_REMETENTE, SENHA)

            for staff_id in staffs:
                user = session.get(User, staff_id)

                if not user or not user.email:
                    continue

                msg = EmailMessage()

                msg["Subject"] = "Treinamento de NR-20"

                msg["From"] = EMAIL_REMETENTE

                msg["To"] = user.email

                if BCC:
                    msg["Bcc"] = BCC

                msg.set_content(body.message)

                smtp.send_message(msg)

    return {"message": "E-mails enviados com sucesso"}


@app.post("/workers/{id}/send-ficha-contabilidade-to-mabecon")
def send_ficha_contabilidade(id: int):
    with Session(engine) as session:
        db_worker_doc = session.exec(
            select(WorkersDocs)
            .where(WorkersDocs.worker_id == id)
            .where(WorkersDocs.doc_title == "Ficha da contabilidade")
        ).first()

        if not db_worker_doc:
            raise HTTPException(status_code=404, detail="Documento não encontrado.")

        EMAIL_REMETENTE = os.environ.get("EMAIL_REMETENTE")

        MABECON_EMAIL = os.environ.get("MABECON_EMAIL")

        SENHA = os.environ.get("SENHA")

        BCC = os.environ.get("BCC")

        filename = "ficha_contabilidade.xls"

        maintype = "application"

        subtype = "vnd.ms-excel"

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_REMETENTE, SENHA)

            msg = EmailMessage()

            msg["Subject"] = "Encaminhamento ficha da contabilidade"

            msg["From"] = EMAIL_REMETENTE

            msg["To"] = MABECON_EMAIL

            if BCC:
                msg["Bcc"] = BCC

            msg.set_content("Encaminhamento de ficha da contabilidade")

            msg.add_attachment(
                db_worker_doc.doc, maintype=maintype, subtype=subtype, filename=filename
            )

            smtp.send_message(msg)

        return {"message": "E-mail enviado com sucesso"}


@app.post("/workers/{id}/send-docs-to-mabecon")
def send_all_docs_to_mabecon(id: int):
    EMAIL_REMETENTE = os.environ["EMAIL_REMETENTE"]

    SENHA = os.environ["SENHA"]

    MABECON_EMAIL = os.environ.get("MABECON_EMAIL")

    BCC = os.environ.get("BCC")

    with Session(engine) as session:
        docs_with_worker = session.exec(
            select(WorkersDocs, Workers)
            .join(Workers, Workers.id == WorkersDocs.worker_id)
            .where(Workers.id == id)
        ).all()

        if not docs_with_worker:
            raise HTTPException(status_code=404, detail="Nenhum documento encontrado.")

        worker_name = docs_with_worker[0][1].name

        docs = [d[0] for d in docs_with_worker]

        msg = EmailMessage()

        msg["Subject"] = (
            f"Encaminhamento de documentos do colaborador {worker_name} para admissão"
        )

        msg["From"] = EMAIL_REMETENTE

        msg["To"] = MABECON_EMAIL

        if BCC:
            msg["Bcc"] = BCC

        msg.set_content(
            f"Segue em anexo os documentos do colaborador {worker_name} para admissão"
        )

        ext_map = {
            "Ficha da contabilidade": (
                "ficha_da_contabilidade.xls",
                "application",
                "vnd.ms-excel",
            )
        }

        for doc in docs:
            filename, maintype, subtype = ext_map.get(
                doc.doc_title, (f"{doc.doc_title}.pdf", "application", "pdf")
            )

            msg.add_attachment(
                doc.doc, maintype=maintype, subtype=subtype, filename=filename
            )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_REMETENTE, SENHA)

            smtp.send_message(msg)

    return {"message": "E-mail enviado com sucesso com todos os documentos."}
