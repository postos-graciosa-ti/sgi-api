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
from sqlalchemy import and_, create_engine, event, extract, func, inspect, text
from sqlalchemy.orm import Session
from sqlmodel import Column, Field, LargeBinary, Session, SQLModel, select
from starlette.status import HTTP_404_NOT_FOUND
from unidecode import unidecode

from controllers.all_subsidiaries_no_review import (
    handle_get_away_return_workers,
    handle_get_workers_without_first_review_in_range_all,
    handle_get_workers_without_second_review_in_range_all,
)
from controllers.applicants import (
    handle_delete_applicants,
    handle_get_applicants,
    handle_get_applicants_notifications,
    handle_patch_applicants,
    handle_post_applicant,
    handle_post_hire_applicants,
)
from controllers.banks import handle_get_banks
from controllers.candidates import (
    handle_get_candidates,
    handle_get_candidates_by_status,
    handle_post_candidate,
)
from controllers.cities import (
    handle_delete_cities,
    handle_get_cities,
    handle_get_cities_by_state,
    handle_get_city_by_id,
    handle_post_new_city,
    handle_put_cities,
)
from controllers.cnh_categories import handle_get_cnh_categories
from controllers.cost_center import (
    handle_delete_cost_center,
    handle_get_cost_center,
    handle_get_cost_center_by_id,
    handle_post_cost_center,
    handle_put_cost_center,
)
from controllers.cost_center_log import (
    handle_get_cost_center_logs,
    handle_post_cost_center_logs,
)
from controllers.dates_events import (
    handle_delete_dates_events,
    handle_get_dates_events,
    handle_get_events_by_date,
    handle_post_dates_events,
)
from controllers.departments import (
    handle_delete_department,
    handle_get_department_by_id,
    handle_get_departments,
    handle_post_department,
    handle_put_department,
)
from controllers.departments_logs import (
    handle_get_departments_logs,
    handle_post_departments_logs,
)
from controllers.functions import (
    handle_delete_function,
    handle_get_functions,
    handle_get_functions_by_subsidiarie,
    handle_get_functions_for_users,
    handle_get_functions_for_workers,
    handle_post_function,
    handle_put_function,
)
from controllers.functions_logs import (
    handle_get_functions_logs,
    handle_post_functions_logs,
)
from controllers.hierarchy_structure import handle_get_hierarchy_structure
from controllers.jobs import (
    handle_delete_job,
    handle_get_jobs,
    handle_get_jobs_by_subsidiarie_id,
    handle_post_job,
)
from controllers.months import handle_get_months
from controllers.nationalities import (
    handle_delete_nationalities,
    handle_get_nationalities,
    handle_post_nationalities,
    handle_put_nationalities,
)
from controllers.parents_type import handle_get_parents_type
from controllers.resignable_reasons import (
    handle_get_resignable_reasons,
    handle_resignable_reasons_report,
)
from controllers.roles import handle_get_roles, handle_get_roles_by_id
from controllers.root import (
    handle_get_docs_info,
    handle_health_check,
    handle_on_startup,
    handle_verify_schema_diff,
)
from controllers.scale import (
    handle_delete_scale,
    handle_get_days_off_quantity,
    handle_get_scales_by_subsidiarie_and_worker_id,
    handle_get_scales_by_subsidiarie_id,
    handle_handle_scale,
    handle_post_scale,
    handle_post_some_workers_scale,
    handle_post_subsidiarie_scale_to_print,
)
from controllers.scales_reports import (
    handle_generate_scale_days_off_report,
    handle_generate_scale_days_on_report,
)
from controllers.school_levels import handle_get_school_levels
from controllers.states import (
    handle_delete_states,
    handle_get_states,
    handle_get_states_by_id,
    handle_get_states_by_nationalitie,
    handle_post_states,
    handle_put_states,
)
from controllers.subsidiaries import (
    handle_delete_subsidiarie,
    handle_get_subsidiarie_by_id,
    handle_get_subsidiaries,
    handle_post_subsidiaries,
)
from controllers.subsidiaries_logs import (
    handle_get_subsidiarie_logs,
    handle_post_subsidiaries_logs,
)
from controllers.subsidiaries_notifications import (
    handle_get_subsidiarie_notifications,
    handle_get_subsidiaries_status,
)
from controllers.turn import (
    handle_delete_turn,
    handle_get_subsidiarie_turns,
    handle_get_turn_by_id,
    handle_get_turns,
    handle_post_turns,
    handle_put_turn,
)
from controllers.turns_logs import handle_get_turns_logs, handle_post_turns_logs
from controllers.users import (
    handle_change_password,
    handle_confirm_password,
    handle_create_user_password,
    handle_delete_user,
    handle_get_test,
    handle_get_user_by_id,
    handle_get_users,
    handle_get_users_roles,
    handle_post_user,
    handle_put_user,
    handle_user_login,
)
from controllers.users_logs import handle_get_logs_user, handle_post_logs_user
from controllers.wage_payment_method import handle_get_wage_payment_method
from controllers.workers import (
    handle_deactivate_worker,
    handle_delete_worker_notation,
    handle_get_active_workers_by_subsidiarie_and_function,
    handle_get_active_workers_by_turn_and_subsidiarie,
    handle_get_worker_by_id,
    handle_get_worker_notations,
    handle_get_workers_by_subsidiarie,
    handle_get_workers_by_subsidiaries_functions_and_turns,
    handle_get_workers_by_turn_and_subsidiarie,
    handle_post_worker,
    handle_post_worker_notation,
    handle_put_worker,
    handle_reactivate_worker,
)
from controllers.workers_logs import (
    handle_get_create_workers_logs,
    handle_get_delete_workers_logs,
    handle_get_update_workers_logs,
    handle_post_create_workers_logs,
    handle_post_delete_workers_logs,
    handle_post_update_workers_logs,
    handle_post_workers_logs,
)
from controllers.workers_parents import (
    handle_delete_workers_parents,
    handle_get_workers_parents,
    handle_post_workers_parents,
)
from controllers.workers_pictures import (
    handle_delete_workers_pictures,
    handle_get_workers_pictures,
    handle_post_workers_pictures,
)
from database.sqlite import engine
from functions.auth import AuthUser, verify_token
from functions.error_handling import error_handler
from keep_alive import keep_alive_function
from middlewares.cors_middleware import add_cors_middleware
from models.applicant_process import ApplicantProcess
from models.applicants import Applicants
from models.applicants_exams import ApplicantsExams
from models.away_reasons import AwayReasons
from models.banks import Banks
from models.candidate import Candidate
from models.checklist import Checklist, ChecklistCreate, ChecklistUpdate
from models.cities import Cities
from models.civil_status import CivilStatus
from models.cnh_categories import CnhCategories
from models.cost_center import CostCenter
from models.cost_center_logs import CostCenterLogs
from models.CustomNotification import CustomNotification
from models.dates_events import DatesEvents
from models.department import Department
from models.department_logs import DepartmentsLogs
from models.discount_reasons import DiscountReasons
from models.docs_checklist import DocsChecklist
from models.ethnicity import Ethnicity
from models.function import Function
from models.function_logs import FunctionLogs
from models.genders import Genders
from models.hierarchy_structure import HierarchyStructure
from models.hollidays_scale import HollidaysScale
from models.indicators import Indicators
from models.indicators_criteria import IndicatorsCriteria
from models.jobs import Jobs
from models.metrics import Metrics
from models.nationalities import Nationalities
from models.neighborhoods import Neighborhoods
from models.open_positions import OpenPositions
from models.parents_type import ParentsType
from models.redirected_to import RedirectedTo
from models.resignable_reasons import ResignableReasons
from models.role import Role
from models.scale import Scale
from models.scale_logs import ScaleLogs
from models.school_levels import SchoolLevels
from models.states import States
from models.subsidiarie import Subsidiarie
from models.subsidiarie_logs import SubsidiarieLogs
from models.system_log import SystemLog
from models.turn import Turn
from models.TurnsLogs import TurnsLogs
from models.user import User
from models.users_logs import UsersLogs
from models.wage_payment_method import WagePaymentMethod
from models.workers import Workers
from models.workers_discounts import WorkersDiscounts
from models.workers_first_review import WorkersFirstReview
from models.workers_logs import WorkersLogs
from models.workers_metrics import WorkersMetrics
from models.workers_parents import WorkersParents
from models.workers_periodic_reviews import WorkersPeriodicReviews
from models.workers_pictures import WorkersPictures
from models.workers_second_review import WorkersSecondReview
from private_routes import private_routes
from public_routes import public_routes
from pyhints.applicants import RecruitProps
from pyhints.no_reviews import SubsidiaryFilter
from pyhints.resignable_reasons import StatusResignableReasonsInput
from pyhints.scales import (
    PostScaleInput,
    PostSomeWorkersScaleInput,
    ScalesPrintInput,
    ScalesReportInput,
    WorkerDeactivateInput,
)
from pyhints.users import (
    ChangeUserPasswordInput,
    ConfirmPassword,
    CreateUserPasswordInput,
    Test,
)
from pyhints.workers import (
    PostWorkerNotationInput,
    WorkerLogCreateInput,
    WorkerLogDeleteInput,
    WorkerLogUpdateInput,
)
from repositories.delete_record import delete_record
from repositories.get_all_records import get_all_records
from repositories.get_record_by_column import get_record_by_column
from repositories.patch_record import patch_record
from repositories.post_record import post_record
from routes.applicants_routes import routes as applicants_routes
from routes.auth_routes import auth_routes
from routes.cities_routes import cities_routes
from routes.nationalities_routes import nationalities_routes
from routes.neighborhoods_routes import neighborhoods_routes
from routes.open_positions_routes import routes as open_positions_routes
from routes.root_routes import root_routes
from routes.scripts_routes import scripts_routes
from routes.states_routes import states_routes
from routes.system_log_routes import system_log_routes
from routes.users_routes import users_routes
from scripts.excel_scraping import handle_excel_scraping
from scripts.rh_sheets import handle_post_scripts_rhsheets
from scripts.sync_workers_data import handle_post_sync_workers_data

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


@app.post("/workers/{worker_id}/autorize-app", dependencies=[Depends(verify_token)])
def post_workers_autorize_app(worker_id: int):
    with Session(engine) as session:
        db_worker = session.get(Workers, worker_id)

        db_worker.app_login = db_worker.cpf

        db_worker.app_password = db_worker.cpf

        session.add(db_worker)

        session.commit()

        session.refresh(db_worker)

        return {"success": True}


# workers


class WorkersAway(BaseModel):
    away_start_date: str
    away_end_date: str
    away_reason_id: int


@app.put("/subsidiaries/{subsidiarie_id}/workers/{worker_id}/away")
def worker_away(subsidiarie_id: int, worker_id: int, worker: WorkersAway):
    with Session(engine) as session:
        get_db_worker = (
            select(Workers)
            .where(Workers.id == worker_id)
            .where(Workers.subsidiarie_id == subsidiarie_id)
        )

        db_worker = session.exec(get_db_worker).first()

        db_worker.is_away = True

        db_worker.away_start_date = (
            worker.away_start_date
            if worker.away_start_date
            else db_worker.away_start_date
        )

        db_worker.away_end_date = (
            worker.away_end_date if worker.away_end_date else db_worker.away_end_date
        )

        db_worker.away_reason_id = (
            worker.away_reason_id if worker.away_reason_id else db_worker.away_reason_id
        )

        start_date = datetime.strptime(worker.away_start_date, "%Y-%m-%d").date()

        end_date = datetime.strptime(worker.away_end_date, "%Y-%m-%d").date()

        away_days = (end_date - start_date).days + 1

        db_worker.time_away = away_days

        session.add(db_worker)

        session.commit()

        session.refresh(db_worker)

        return db_worker


@app.put("/subsidiaries/{subsidiarie_id}/workers/{worker_id}/away-return")
def sla(subsidiarie_id: int, worker_id: int):
    with Session(engine) as session:
        get_db_worker = (
            select(Workers)
            .where(Workers.id == worker_id)
            .where(Workers.subsidiarie_id == subsidiarie_id)
        )

        db_worker = session.exec(get_db_worker).first()

        db_worker.is_away = False

        session.add(db_worker)

        session.commit()

        return db_worker


# school levels


@app.get("/school-levels")
def get_school_levels():
    return handle_get_school_levels()


# banks


@app.get("/banks")
def get_banks():
    return handle_get_banks()


class WorkersByTurnAndFunctionModel(BaseModel):
    turns: list
    functions: list


@app.post("/subsidiaries/{subsidiarie_id}/workers-by-turn-and-function")
def get_workers_by_turn_and_function(
    subsidiarie_id: int, data: WorkersByTurnAndFunctionModel
):
    with Session(engine) as session:
        result = []

        turns = data.turns

        functions = data.functions

        for turn in turns:
            for function in functions:
                workers = session.exec(
                    select(Workers)
                    .where(Workers.subsidiarie_id == subsidiarie_id)
                    .where(Workers.turn_id == turn)
                    .where(Workers.function_id == function)
                ).all()

                result.extend(workers)

        return result


# parents type


@app.get("/parents-type")
def get_parents_type():
    return handle_get_parents_type()


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


from models.service import Service
from models.tickets import Tickets
from models.tickets_comments import TicketsComments


@app.get("/services")
def get_services():
    with Session(engine) as session:
        services = session.exec(select(Service)).all()

        return services


from fastapi import HTTPException


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


from datetime import date


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


# @app.get("/subsidiaries/{subsidiarie_id}/workers/{worker_id}")
# def sla(subsidiarie_id: int, worker_id: int):
#     today = datetime.today().date()

#     with Session(engine) as session:
#         first_review = session.exec(
#             select(Workers)
#             .where(Workers.subsidiarie_id == subsidiarie_id)
#             .where(Workers.id == worker_id)
#             .where(Workers.first_review_date >= today)
#         ).first()

#         can_open_first_review_modal = (
#             True
#             if session.exec(
#                 select(Workers)
#                 .where(Workers.subsidiarie_id == subsidiarie_id)
#                 .where(Workers.id == worker_id)
#                 .where(Workers.first_review_date >= today)
#             ).first()
#             else False
#         )

#         second_review = session.exec(
#             select(Workers)
#             .where(Workers.subsidiarie_id == subsidiarie_id)
#             .where(Workers.id == worker_id)
#             .where(Workers.second_review_date >= today)
#         ).first()

#         can_open_second_review_modal = (
#             True
#             if session.exec(
#                 select(Workers)
#                 .where(Workers.subsidiarie_id == subsidiarie_id)
#                 .where(Workers.id == worker_id)
#                 .where(Workers.second_review_date >= today)
#             ).first()
#             else False
#         )

#         return {
#             "first_review": first_review,
#             "second_review": second_review,
#             "can_open_first_review_modal": can_open_first_review_modal,
#             "can_open_second_review_modal": can_open_second_review_modal,
#         }


# class WorkersFieldsByTurnAndFunctionInput(BaseModel):
#     fields: list


# @app.post(
#     "/subsidiaries/{subsidiarie_id}/workers/functions/{function_id}/turns/{turn_id}"
# )
# def workers_fields_by_turn_and_function(
#     subsidiarie_id: int,
#     function_id: int,
#     turn_id: int,
#     input: WorkersFieldsByTurnAndFunctionInput,
# ):
#     with Session(engine) as session:
#         workers = session.exec(
#             select(Workers, Function, Turn, CostCenter, Department)
#             .join(Function, Workers.function_id == Function.id)
#             .join(Turn, Workers.turn_id == Turn.id)
#             .join(CostCenter, Workers.cost_center_id == CostCenter.id)
#             .join(Department, Workers.department_id == Department.id)
#             .where(Workers.subsidiarie_id == subsidiarie_id)
#             .where(Workers.function_id == function_id)
#             .where(Workers.turn_id == turn_id)
#         ).all()

#         result = [
#             {
#                 "esocial": worker.esocial,
#                 "enrolment": worker.enrolment,
#                 "sales_code": worker.sales_code,
#                 "timecode": worker.timecode,
#                 "worker_name": worker.name,
#                 "function_name": function.name,
#                 "turn_name": turn.name,
#                 "cost_center_name": cost_center.name,
#                 "department_name": department.name,
#                 "admission_date": worker.admission_date,
#             }
#             for worker, function, turn, cost_center, department in workers
#         ]

#         return result

# if not workers:
#     return []

# valid_fields = {column.name for column in Workers.__table__.columns}

# requested_fields = [field for field in input.fields if field in valid_fields]

# result = [
#     {field: getattr(worker, field) for field in requested_fields}
#     for worker in workers
# ]

# return workers


# @app.get("/subsidiaries/{id}/get-nr20-list")
# def get_nr_list_by_subsidiarie(id: int):
#     today = date.today()

#     first_day = today.replace(day=1)

#     last_day = today.replace(day=1).replace(month=today.month + 1) - timedelta(days=1)

#     with Session(engine) as session:
#         nr_list = session.exec(
#             select(Workers)
#             .where(Workers.subsidiarie_id == id)
#             .where(Workers.second_review_date.between(first_day, last_day))
#         ).all()

#         return {"nr_list": nr_list, "first_day": first_day, "last_day": last_day}
