import io
import json
import os
import smtplib
import threading
from datetime import datetime, timedelta
from email.message import EmailMessage
from functools import wraps
from io import BytesIO
from typing import Annotated, Any, Callable, Dict, List, Optional, Set

import httpx
import pandas as pd
import PyPDF2
import requests
from cachetools import TTLCache
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, EmailStr
from PyPDF2 import PdfReader, PdfWriter
from sqlalchemy import and_, create_engine, event, inspect, text
from sqlalchemy.orm import Session
from sqlmodel import Column, Field, LargeBinary, Session, SQLModel, select

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
from controllers.hollidays_scale import (
    handle_delete_hollidays_scale,
    handle_get_hollidays_scale,
    handle_post_hollidays_scale,
)
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
from controllers.roles import handle_get_roles
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
from database.sqlite import engine
from functions.auth import verify_token
from functions.error_handling import error_handler
from keep_alive import keep_alive_function
from middlewares.cors_middleware import add_cors_middleware
from models.applicants import Applicants
from models.away_reasons import AwayReasons
from models.banks import Banks
from models.candidate import Candidate
from models.cities import Cities
from models.civil_status import CivilStatus
from models.cnh_categories import CnhCategories
from models.cost_center import CostCenter
from models.cost_center_logs import CostCenterLogs
from models.dates_events import DatesEvents
from models.department import Department
from models.department_logs import DepartmentsLogs
from models.ethnicity import Ethnicity
from models.function import Function
from models.function_logs import FunctionLogs
from models.genders import Genders
from models.hierarchy_structure import HierarchyStructure
from models.hollidays_scale import HollidaysScale
from models.jobs import Jobs
from models.nationalities import Nationalities
from models.neighborhoods import Neighborhoods
from models.parents_type import ParentsType
from models.resignable_reasons import ResignableReasons
from models.role import Role
from models.scale import Scale
from models.scale_logs import ScaleLogs
from models.school_levels import SchoolLevels
from models.states import States
from models.subsidiarie import Subsidiarie
from models.subsidiarie_logs import SubsidiarieLogs
from models.turn import Turn
from models.TurnsLogs import TurnsLogs
from models.user import User
from models.users_logs import UsersLogs
from models.wage_payment_method import WagePaymentMethod
from models.workers import Workers
from models.workers_first_review import WorkersFirstReview
from models.workers_logs import WorkersLogs
from models.workers_parents import WorkersParents
from models.workers_second_review import WorkersSecondReview
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
from pyhints.turns import PutTurn
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
from scripts.excel_scraping import handle_excel_scraping
from scripts.rh_sheets import handle_post_scripts_rhsheets

# pre settings

load_dotenv()

app = FastAPI()

add_cors_middleware(app)

threading.Thread(target=keep_alive_function, daemon=True).start()

# startup function


@app.on_event("startup")
def on_startup():
    return handle_on_startup()


# utils public routes


@app.get("/")
def get_docs_info():
    return handle_get_docs_info()


@app.get("/health-check")
def health_check():
    return handle_health_check()


@app.get("/verify-schema-diff")
def verify_schema_diff():
    return handle_verify_schema_diff()


# users public routes


@app.post("/users/login")
def user_login(user: User):
    return handle_user_login(user)


@app.post("/users/create-password")
def create_user_password(userData: CreateUserPasswordInput):
    return handle_create_user_password(userData)


# scripts public routes


@app.post("/subsidiaries/{id}/scripts/excel-scraping")
async def excel_scraping(id: int, file: UploadFile = File(...)):
    return await handle_excel_scraping(id, file)


@app.post("/scripts/rhsheets")
async def post_scripts_rhsheets(
    discountList: Annotated[str, Form()],
    file: UploadFile = File(...),
):
    return await handle_post_scripts_rhsheets(discountList, file)


# users


@app.get("/users", dependencies=[Depends(verify_token)])
@error_handler
def get_users():
    return handle_get_users()


@app.get("/users/{id}", dependencies=[Depends(verify_token)])
@error_handler
def get_user_by_id(id: int):
    return handle_get_user_by_id(id)


@app.get("/users_roles", dependencies=[Depends(verify_token)])
@error_handler
def get_users_roles():
    return handle_get_users_roles()


@app.post("/users", dependencies=[Depends(verify_token)])
@error_handler
def post_user(user: User):
    return handle_post_user(user)


@app.put("/users/{id}", dependencies=[Depends(verify_token)])
@error_handler
def put_user(id: int, user: User):
    return handle_put_user(id, user)


@app.delete("/users/{id}", dependencies=[Depends(verify_token)])
@error_handler
def delete_user(id: int):
    return handle_delete_user(id)


@app.post("/test", dependencies=[Depends(verify_token)])
@error_handler
def test(arr: Test):
    return handle_get_test(arr)


@app.post("/confirm-password", dependencies=[Depends(verify_token)])
@error_handler
def confirm_password(userData: ConfirmPassword):
    return handle_confirm_password(userData)


@app.post("/users/change-password", dependencies=[Depends(verify_token)])
@error_handler
def change_password(userData: ChangeUserPasswordInput):
    return handle_change_password(userData)


# user logs


@app.get("/logs/users", dependencies=[Depends(verify_token)])
@error_handler
def get_logs_user():
    return handle_get_logs_user()


@app.post("/logs/users", dependencies=[Depends(verify_token)])
@error_handler
def post_logs_user(users_logs: UsersLogs):
    return handle_post_logs_user(users_logs)


# months


@app.get("/months", dependencies=[Depends(verify_token)])
@error_handler
def get_months():
    return handle_get_months()


# subsidiaries


@app.get("/subsidiaries", dependencies=[Depends(verify_token)])
@error_handler
def get_subsidiaries():
    return handle_get_subsidiaries()


@app.get("/subsidiaries/{id}", dependencies=[Depends(verify_token)])
@error_handler
def get_subsidiarie_by_id(id: int):
    return handle_get_subsidiarie_by_id(id)


@app.post("/subsidiaries", dependencies=[Depends(verify_token)])
@error_handler
def post_subsidiaries(formData: Subsidiarie):
    return handle_post_subsidiaries(formData)


@app.put("/subsidiaries/{id}", dependencies=[Depends(verify_token)])
@error_handler
def put_subsidiarie(id: int, subsidiarie: Subsidiarie):
    with Session(engine) as session:
        db_subsidiarie = session.exec(
            select(Subsidiarie).where(Subsidiarie.id == id)
        ).first()

        if subsidiarie.name and subsidiarie.name != db_subsidiarie.name:
            db_subsidiarie.name = subsidiarie.name

        if subsidiarie.adress and subsidiarie.adress != db_subsidiarie.adress:
            db_subsidiarie.adress = subsidiarie.adress

        if subsidiarie.phone and subsidiarie.phone != db_subsidiarie.phone:
            db_subsidiarie.phone = subsidiarie.phone

        if subsidiarie.email and subsidiarie.email != db_subsidiarie.email:
            db_subsidiarie.email = subsidiarie.email

        if (
            subsidiarie.coordinator is not None
            and subsidiarie.coordinator != db_subsidiarie.coordinator
        ):
            db_subsidiarie.coordinator = subsidiarie.coordinator

        if (
            subsidiarie.manager is not None
            and subsidiarie.manager != db_subsidiarie.manager
        ):
            db_subsidiarie.manager = subsidiarie.manager

        session.add(db_subsidiarie)

        session.commit()

        session.refresh(db_subsidiarie)

        return db_subsidiarie


@app.delete("/subsidiaries/{id}", dependencies=[Depends(verify_token)])
@error_handler
def delete_subsidiaries(id: int):
    return handle_delete_subsidiarie(id)


# subsidiaries notifications


@app.get("/subsidiaries/{id}/notifications", dependencies=[Depends(verify_token)])
@error_handler
async def get_subsidiarie_notifications(id: int):
    return await handle_get_subsidiarie_notifications(id)


@app.get("/subsidiaries/{id}/workers-status", dependencies=[Depends(verify_token)])
@error_handler
def get_subsidiaries_status(id: int):
    handle_get_subsidiaries_status(id)


# subsidiaries logs


@app.get("/subsidiaries-logs", dependencies=[Depends(verify_token)])
@error_handler
def get_subsidiarie_logs():
    return handle_get_subsidiarie_logs()


@app.post("/subsidiaries/logs", dependencies=[Depends(verify_token)])
@error_handler
def post_subsidiaries_logs(subsidiarie_log: SubsidiarieLogs):
    return handle_post_subsidiaries_logs(subsidiarie_log)


# turns


@app.get("/subsidiaries/{id}/turns", dependencies=[Depends(verify_token)])
@error_handler
def get_subsidiarie_turns(id: int):
    return handle_get_subsidiarie_turns(id)


@app.get("/turns", dependencies=[Depends(verify_token)])
@error_handler
def get_turns():
    return handle_get_turns()


@app.get("/turns/{id}", dependencies=[Depends(verify_token)])
@error_handler
def get_turn_by_id(id: int):
    return handle_get_turn_by_id(id)


@app.post("/turns", dependencies=[Depends(verify_token)])
@error_handler
def post_turns(formData: Turn):
    return handle_post_turns(formData)


@app.put("/turns/{id}", dependencies=[Depends(verify_token)])
@error_handler
def put_turn(id: int, formData: PutTurn):
    return handle_put_turn(id, formData)


@app.delete("/turns/{id}", dependencies=[Depends(verify_token)])
@error_handler
def delete_turn(id: int):
    return handle_delete_turn(id)


# turns logs


@app.get("/subsidiaries/{id}/logs/turns", dependencies=[Depends(verify_token)])
@error_handler
def get_turns_logs(id: int):
    return handle_get_turns_logs(id)


@app.post("/subsidiaries/{id}/logs/turns", dependencies=[Depends(verify_token)])
@error_handler
def post_turns_logs(id: int, turn_log: TurnsLogs):
    return handle_post_turns_logs(id, turn_log)


# workers


@app.get("/workers/{id}", dependencies=[Depends(verify_token)])
@error_handler
def get_worker_by_id(id: int):
    return handle_get_worker_by_id(id)


@app.get(
    "/workers/turns/{turn_id}/subsidiarie/{subsidiarie_id}",
    dependencies=[Depends(verify_token)],
)
@error_handler
def get_workers_by_turn_and_subsidiarie(turn_id: int, subsidiarie_id: int):
    return handle_get_workers_by_turn_and_subsidiarie(turn_id, subsidiarie_id)


@app.get(
    "/workers/on-track/turn/{turn_id}/subsidiarie/{subsidiarie_id}",
    dependencies=[Depends(verify_token)],
)
@error_handler
def get_active_workers_by_turn_and_subsidiarie(turn_id: int, subsidiarie_id: int):
    return handle_get_active_workers_by_turn_and_subsidiarie(turn_id, subsidiarie_id)


@app.get(
    "/workers/active/subsidiarie/{subsidiarie_id}/function/{function_id}",
    dependencies=[Depends(verify_token)],
)
@error_handler
def get_active_workers_by_subsidiarie_and_function(
    subsidiarie_id: int, function_id: int
):
    return handle_get_active_workers_by_subsidiarie_and_function(
        subsidiarie_id, function_id
    )


@app.get("/workers/subsidiarie/{subsidiarie_id}", dependencies=[Depends(verify_token)])
def get_workers_by_subsidiarie(subsidiarie_id: int):
    return handle_get_workers_by_subsidiarie(subsidiarie_id)


@app.get(
    "/workers/subsidiaries/{subsidiarie_id}/functions/{function_id}/turns/{turn_id}",
    dependencies=[Depends(verify_token)],
)
@error_handler
def get_workers_by_subsidiaries_functions_and_turns(
    subsidiarie_id: int, function_id: int, turn_id: int
):
    return handle_get_workers_by_subsidiaries_functions_and_turns(
        subsidiarie_id, function_id, turn_id
    )


@app.get(
    "/subsidiaries/{subsidiarie_id}/turns/{turn_id}/functions/{function_id}/workers",
    dependencies=[Depends(verify_token)],
)
@error_handler
def get_workers_by_turn_and_function(
    subsidiarie_id: int, turn_id: int, function_id: int
):
    with Session(engine) as session:
        workers = session.exec(
            select(Workers)
            .where(Workers.subsidiarie_id == subsidiarie_id)
            .where(Workers.turn_id == turn_id)
            .where(Workers.function_id == function_id)
        ).all()

        return workers


@app.get(
    "/subsidiaries/{subsidiarie_id}/turns/{turn_id}/workers",
    dependencies=[Depends(verify_token)],
)
@error_handler
def get_workers_by_turn(subsidiarie_id: int, turn_id: int):
    with Session(engine) as session:
        workers = session.exec(
            select(Workers)
            .where(Workers.subsidiarie_id == subsidiarie_id)
            .where(Workers.turn_id == turn_id)
        ).all()

        return workers


@app.post("/workers")
def post_worker(worker: Workers):
    admission_date = datetime.strptime(worker.admission_date, "%Y-%m-%d").date()

    first_review = admission_date + relativedelta(months=1)

    second_review = admission_date + relativedelta(months=2)

    worker.first_review_date = first_review.strftime("%Y-%m-%d")

    worker.second_review_date = second_review.strftime("%Y-%m-%d")

    with Session(engine) as session:
        session.add(worker)

        session.commit()

        session.refresh(worker)

        return worker


@app.put("/workers/{id}", dependencies=[Depends(verify_token)])
@error_handler
def put_worker(id: int, worker: Workers):
    return handle_put_worker(id, worker)


@app.put("/workers/{id}/deactivate", dependencies=[Depends(verify_token)])
@error_handler
def deactivate_worker(id: int, worker: WorkerDeactivateInput):
    return handle_deactivate_worker(id, worker)


@app.put("/workers/{id}/reactivate", dependencies=[Depends(verify_token)])
@error_handler
def reactivate_worker(id: int):
    return handle_reactivate_worker(id)


# workers logs


@app.get("/logs/subsidiaries/{id}/workers", dependencies=[Depends(verify_token)])
@error_handler
def get_workers_logs(id: int):
    with Session(engine) as session:
        query = select(WorkersLogs).where(WorkersLogs.subsidiarie_id == id)

        workers_logs = session.exec(query).all()

        return workers_logs


@app.post("/logs/subsidiaries/{id}/workers", dependencies=[Depends(verify_token)])
@error_handler
def post_workers_logs(id: int, workers_log: WorkersLogs):
    return handle_post_workers_logs(id, workers_log)


# workers logs create


@app.get("/logs/subsidiaries/{id}/workers/create", dependencies=[Depends(verify_token)])
@error_handler
def get_create_workers_logs(id: int):
    return handle_get_create_workers_logs(id)


@app.post(
    "/logs/subsidiaries/{id}/workers/create", dependencies=[Depends(verify_token)]
)
@error_handler
def post_create_workers_logs(id: int, worker_log: WorkerLogCreateInput):
    return handle_post_create_workers_logs(id, worker_log)


# workers logs update


@app.get("/logs/subsidiaries/{id}/workers/update", dependencies=[Depends(verify_token)])
@error_handler
def get_update_workers_logs(id: int):
    return handle_get_update_workers_logs(id)


@app.post(
    "/logs/subsidiaries/{id}/workers/update", dependencies=[Depends(verify_token)]
)
@error_handler
def post_update_workers_logs(id: int, worker_log: WorkerLogUpdateInput):
    return handle_post_update_workers_logs(id, worker_log)


# workers logs delete


@app.get("/logs/subsidiaries/{id}/workers/delete", dependencies=[Depends(verify_token)])
@error_handler
def get_delete_workers_logs(id: int):
    return handle_get_delete_workers_logs(id)


@app.post(
    "/logs/subsidiaries/{id}/workers/delete", dependencies=[Depends(verify_token)]
)
@error_handler
def post_delete_workers_logs(id: int, worker_log: WorkerLogDeleteInput):
    return handle_post_delete_workers_logs(id, worker_log)


# workers notations


@app.get("/workers/{id}/notations", dependencies=[Depends(verify_token)])
@error_handler
def get_worker_notations(id: int):
    return handle_get_worker_notations(id)


@app.post("/workers/{id}/notations", dependencies=[Depends(verify_token)])
@error_handler
def post_worker_notation(id: int, data: PostWorkerNotationInput):
    return handle_post_worker_notation(id, data)


@app.delete("/workers-notations/{id}", dependencies=[Depends(verify_token)])
@error_handler
def delete_worker_notation(id: int):
    return handle_delete_worker_notation(id)


# functions


@app.get("/subsidiaries/{id}/functions", dependencies=[Depends(verify_token)])
@error_handler
def get_functions_by_subsidiarie(id: int):
    return handle_get_functions_by_subsidiarie(id)


@app.get("/functions", dependencies=[Depends(verify_token)])
@error_handler
def get_functions():
    return handle_get_functions()


@app.get("/functions/for-users", dependencies=[Depends(verify_token)])
@error_handler
def get_functions_for_users():
    return handle_get_functions_for_users()


@app.get("/functions/for-workers", dependencies=[Depends(verify_token)])
@error_handler
def get_functions_for_users():
    return handle_get_functions_for_workers()


@app.post("/functions", dependencies=[Depends(verify_token)])
@error_handler
def post_function(function: Function):
    return handle_post_function(function)


@app.put("/functions/{id}", dependencies=[Depends(verify_token)])
@error_handler
def put_function(id: int, function: Function):
    return handle_put_function(id, function)


@app.delete("/functions/{id}", dependencies=[Depends(verify_token)])
@error_handler
def delete_function(id: int):
    return handle_delete_function(id)


# functions logs


@app.get("/subsidiaries/{id}/functions/logs", dependencies=[Depends(verify_token)])
@error_handler
def get_functions_logs(id: int):
    return handle_get_functions_logs(id)


@app.post("/subsidiaries/{id}/functions/logs", dependencies=[Depends(verify_token)])
@error_handler
def post_functions_logs(id: int, function_log: FunctionLogs):
    return handle_post_functions_logs(id, function_log)


# jobs


@app.get("/jobs", dependencies=[Depends(verify_token)])
@error_handler
def get_jobs():
    return handle_get_jobs()


@app.get("/jobs/subsidiarie/{subsidiarie_id}", dependencies=[Depends(verify_token)])
@error_handler
def get_jobs_by_subsidiarie_id(subsidiarie_id: int):
    return handle_get_jobs_by_subsidiarie_id(subsidiarie_id)


@app.post("/jobs", dependencies=[Depends(verify_token)])
@error_handler
def post_job(job: Jobs):
    return handle_post_job(job)


@app.delete("/jobs/{job_id}", dependencies=[Depends(verify_token)])
@error_handler
def delete_job(job_id: int):
    return handle_delete_job(job_id)


# roles


@app.get("/roles", dependencies=[Depends(verify_token)])
@error_handler
def get_roles():
    return handle_get_roles()


@app.get("/roles/{id}", dependencies=[Depends(verify_token)])
@error_handler
def get_roles_by_id(id: int):
    with Session(engine) as session:
        role = session.exec(select(Role).where(Role.id == id)).first()

        return role


# candidates


@app.get("/candidates", dependencies=[Depends(verify_token)])
@error_handler
def get_candidates():
    return handle_get_candidates()


@app.get("/candidates/status/{id}", dependencies=[Depends(verify_token)])
@error_handler
def get_candidates_by_status(id: int):
    return handle_get_candidates_by_status(id)


@app.post("/candidates", dependencies=[Depends(verify_token)])
@error_handler
def post_candidate(candidate: Candidate):
    return handle_post_candidate(candidate)


# scales


@app.get("/scales/subsidiaries/{subsidiarie_id}", dependencies=[Depends(verify_token)])
@error_handler
def get_scales_by_subsidiarie_id(subsidiarie_id: int):
    return handle_get_scales_by_subsidiarie_id(subsidiarie_id)


@app.get(
    "/scales/subsidiaries/{subsidiarie_id}/workers/{worker_id}",
    dependencies=[Depends(verify_token)],
)
@error_handler
def get_scales_by_subsidiarie_and_worker_id(subsidiarie_id: int, worker_id: int):
    return handle_get_scales_by_subsidiarie_and_worker_id(subsidiarie_id, worker_id)


@app.get("/scales/day-off/quantity", dependencies=[Depends(verify_token)])
@error_handler
def get_days_off_quantity():
    return handle_get_days_off_quantity()


@app.post("/scales", dependencies=[Depends(verify_token)])
@error_handler
def post_scale(form_data: PostScaleInput):
    return handle_post_scale(form_data)


@app.post("/scales/some-workers", dependencies=[Depends(verify_token)])
@error_handler
def post_some_workers_scale(form_data: PostSomeWorkersScaleInput):
    return handle_post_some_workers_scale(form_data)


@app.post("/delete-scale", dependencies=[Depends(verify_token)])
@error_handler
def handle_scale(form_data: PostScaleInput):
    return handle_handle_scale(form_data)


@app.delete(
    "/scales/{scale_id}/subsidiaries/{subsidiarie_id}",
    dependencies=[Depends(verify_token)],
)
@error_handler
def delete_scale(scale_id: int, subsidiarie_id: int):
    return handle_delete_scale(scale_id, subsidiarie_id)


# scale logs


@app.get("/subsidiaries/{id}/scales/logs", dependencies=[Depends(verify_token)])
@error_handler
def get_scales_logs(id: int):
    with Session(engine) as session:
        scales_logs = session.exec(
            select(ScaleLogs)
            .where(ScaleLogs.subsidiarie_id == id)
            .order_by(ScaleLogs.id.desc())
        ).all()

        return scales_logs


@app.post("/subsidiaries/{id}/scales/logs", dependencies=[Depends(verify_token)])
@error_handler
def post_scales_logs(id: int, scale_log: ScaleLogs):
    with Session(engine) as session:
        scale_log.subsidiarie_id = id

        session.add(scale_log)

        session.commit()

        session.refresh(scale_log)

        return scale_log


# scale reports


@app.post(
    "/reports/subsidiaries/{subsidiarie_id}/scales/days-on",
    dependencies=[Depends(verify_token)],
)
async def generate_scale_days_on_report(subsidiarie_id: int, input: ScalesReportInput):
    return await handle_generate_scale_days_on_report(subsidiarie_id, input)


@app.post(
    "/reports/subsidiaries/{subsidiarie_id}/scales/days-off",
    dependencies=[Depends(verify_token)],
)
async def generate_scale_days_off_report(subsidiarie_id: int, input: ScalesReportInput):
    return await handle_generate_scale_days_off_report(subsidiarie_id, input)


# scales print


@app.post("/subsidiaries/{id}/scales/print", dependencies=[Depends(verify_token)])
def post_subsidiarie_scale_to_print(id: int, scales_print_input: ScalesPrintInput):
    return handle_post_subsidiarie_scale_to_print(id, scales_print_input)


# cost center


@app.get("/cost-center", dependencies=[Depends(verify_token)])
@error_handler
def get_cost_center():
    return handle_get_cost_center()


@app.get("/cost-center/{id}", dependencies=[Depends(verify_token)])
@error_handler
def get_cost_center_by_id(id: int):
    return handle_get_cost_center_by_id(id)


@app.post("/cost-center", dependencies=[Depends(verify_token)])
@error_handler
def post_cost_center(cost_center_input: CostCenter):
    return handle_post_cost_center(cost_center_input)


@app.put("/cost-center/{id}", dependencies=[Depends(verify_token)])
@error_handler
def put_cost_center(id: int, cost_center_input: CostCenter):
    return handle_put_cost_center(id, cost_center_input)


@app.delete("/cost-center/{id}", dependencies=[Depends(verify_token)])
@error_handler
def delete_cost_center(id: int):
    return handle_delete_cost_center(id)


# cost center logs


@app.get("/subsidiaries/{id}/logs/costs-centers")
@error_handler
def get_cost_center_logs(id: int):
    return handle_get_cost_center_logs(id)


@app.post("/subsidiaries/{id}/logs/costs-centers", dependencies=[Depends(verify_token)])
@error_handler
def post_cost_center_logs(id: int, cost_center_log: CostCenterLogs):
    return handle_post_cost_center_logs(id, cost_center_log)


# department


@app.get("/departments", dependencies=[Depends(verify_token)])
@error_handler
def get_departments():
    return handle_get_departments()


@app.get("/departments/{id}", dependencies=[Depends(verify_token)])
@error_handler
def get_department_by_id(id: int):
    return handle_get_department_by_id(id)


@app.post("/departments", dependencies=[Depends(verify_token)])
@error_handler
def post_department(department_input: Department):
    return handle_post_department(department_input)


@app.put("/departments/{id}", dependencies=[Depends(verify_token)])
@error_handler
def put_department(id: int, department_input: Department):
    return handle_put_department(id, department_input)


@app.delete("/departments/{id}", dependencies=[Depends(verify_token)])
@error_handler
def delete_department(id: int):
    return handle_delete_department(id)


# department logs


@app.get("/subsidiaries/{id}/logs/departments", dependencies=[Depends(verify_token)])
@error_handler
def get_departments_logs(id: int):
    return handle_get_departments_logs(id)


@app.post("/subsidiaries/{id}/logs/departments", dependencies=[Depends(verify_token)])
@error_handler
def post_departments_logs(id: int, department_logs_input: DepartmentsLogs):
    return handle_post_departments_logs(id, department_logs_input)


# resignable reasons


@app.get("/resignable-reasons", dependencies=[Depends(verify_token)])
@error_handler
def get_resignable_reasons():
    return handle_get_resignable_reasons()


# resignable reasons reports


@app.post("/resignable-reasons/report", dependencies=[Depends(verify_token)])
@error_handler
def get_resignable_reasons_report(input: StatusResignableReasonsInput):
    return handle_resignable_reasons_report(input)


# applicants


@app.get("/applicants", dependencies=[Depends(verify_token)])
def get_applicants():
    return handle_get_applicants()


@app.post("/applicants", dependencies=[Depends(verify_token)])
def post_applicant(applicant: Applicants):
    return handle_post_applicant(applicant)


@app.patch("/applicants/{id}", dependencies=[Depends(verify_token)])
def patch_applicants(id: int, applicant: Applicants):
    return handle_patch_applicants(id, applicant)


@app.delete("/applicants/{id}", dependencies=[Depends(verify_token)])
def delete_applicants(id: int):
    return handle_delete_applicants(id)


# hire applicants


@app.post("/applicants/hire", dependencies=[Depends(verify_token)])
def post_hire_applicants(recruit: RecruitProps):
    return handle_post_hire_applicants(recruit)


# applicants notifications


@app.get("/users/{id}/applicants/notifications", dependencies=[Depends(verify_token)])
def get_applicants_notifications(id: int):
    return handle_get_applicants_notifications(id)


# worker first review


@app.get("/workers/{id}/first-review")
def get_worker_first_review(id: int):
    with Session(engine) as session:
        db_worker_first_review = session.exec(
            select(WorkersFirstReview).where(WorkersFirstReview.worker_id == id)
        ).one()

        return db_worker_first_review


@app.post("/workers/{id}/first-review")
def post_worker_first_review(id: int, worker_first_review: WorkersFirstReview):
    worker_first_review.worker_id = id

    with Session(engine) as session:
        session.add(worker_first_review)

        session.commit()

        session.refresh(worker_first_review)

        return worker_first_review


@app.get("/subsidiaries/{subsidiarie_id}/workers/first-review/notification")
def get_workers_first_review(subsidiarie_id: int):
    with Session(engine) as session:
        today = date.today()

        start_of_week = (today - timedelta(days=today.weekday())).isoformat()

        end_of_week = (
            datetime.fromisoformat(start_of_week) + timedelta(days=6)
        ).isoformat()

        first_review_notifications = (
            session.exec(
                select(WorkersFirstReview, User, Workers)
                .join(User, WorkersFirstReview.realized_by == User.id)
                .join(Workers, WorkersFirstReview.worker_id == Workers.id)
                .where(Workers.subsidiarie_id == subsidiarie_id)
                .where(WorkersFirstReview.realized_in >= start_of_week)
                .where(WorkersFirstReview.realized_in <= end_of_week)
            )
            .mappings()
            .all()
        )

        return first_review_notifications


# worker second review


@app.get("/workers/{id}/second-review")
def get_worker_first_review(id: int):
    with Session(engine) as session:
        db_worker_first_review = session.exec(
            select(WorkersSecondReview).where(WorkersSecondReview.worker_id == id)
        ).one()

        return db_worker_first_review


@app.post("/workers/{id}/second-review")
def post_worker_first_review(id: int, worker_second_review: WorkersSecondReview):
    worker_second_review.worker_id = id

    with Session(engine) as session:
        session.add(worker_second_review)

        session.commit()

        session.refresh(worker_second_review)

        return worker_second_review


@app.get("/subsidiaries/{subsidiarie_id}/workers/second-review/notification")
def get_workers_second_review(subsidiarie_id: int):
    with Session(engine) as session:
        today = date.today()

        start_of_week = (today - timedelta(days=today.weekday())).isoformat()

        end_of_week = (
            datetime.fromisoformat(start_of_week) + timedelta(days=6)
        ).isoformat()

        second_review_notifications = (
            session.exec(
                select(WorkersSecondReview, User, Workers)
                .join(User, WorkersSecondReview.realized_by == User.id)
                .join(Workers, WorkersSecondReview.worker_id == Workers.id)
                .where(Workers.subsidiarie_id == subsidiarie_id)
                .where(WorkersSecondReview.realized_in >= start_of_week)
                .where(WorkersSecondReview.realized_in <= end_of_week)
            )
            .mappings()
            .all()
        )

        return second_review_notifications


@app.get(
    "/subsidiaries/{subsidiarie_id}/workers/functions/{function_id}/turns/{turn_id}"
)
def get_workers_by_functions(subsidiarie_id: int, function_id: int, turn_id: int):
    with Session(engine) as session:
        workers_by_function = session.exec(
            select(
                Workers.enrolment.label("enrolment"),
                Workers.name.label("name"),
                CostCenter.name.label("cost_center"),
                Department.name.label("department"),
            )
            .join(CostCenter, Workers.cost_center_id == CostCenter.id)
            .join(Department, Workers.department_id == Department.id)
            .where(Workers.subsidiarie_id == subsidiarie_id)
            .where(Workers.is_active == True)
            .where(Workers.function_id == function_id)
            .where(Workers.turn_id == turn_id)
        ).all()

        return [
            {
                "enrolment": worker.enrolment,
                "name": worker.name,
                "cost_center": worker.cost_center,
                "department": worker.department,
            }
            for worker in workers_by_function
        ]


from datetime import datetime

from dateutil.relativedelta import relativedelta
from fastapi import FastAPI
from sqlmodel import Session, select


@app.get("/subsidiaries/{subsidiarie_id}/workers/experience-time-no-first-review")
def get_workers_without_first_review_in_range(subsidiarie_id: int):
    with Session(engine) as session:
        today = datetime.today()

        start_of_week = today - relativedelta(days=today.weekday())

        end_of_week = start_of_week + relativedelta(days=6)

        start_of_week_str = start_of_week.strftime("%Y-%m-%d")

        end_of_week_str = end_of_week.strftime("%Y-%m-%d")

        workers_without_first_review = session.exec(
            select(Workers)
            .where(Workers.subsidiarie_id == subsidiarie_id)
            .where(Workers.first_review_date >= start_of_week_str)
            .where(Workers.first_review_date <= end_of_week_str)
            .where(
                ~Workers.id.in_(
                    select(WorkersFirstReview.worker_id).where(
                        WorkersFirstReview.worker_id == Workers.id
                    )
                )
            )
        ).all()

        return {
            "workers": workers_without_first_review,
            "start_of_week": start_of_week,
            "end_of_week": end_of_week,
        }


@app.get("/subsidiaries/{subsidiarie_id}/workers/experience-time-no-second-review")
def get_workers_without_second_review_in_range(subsidiarie_id: int):
    with Session(engine) as session:
        today = datetime.today()

        start_of_week = today - timedelta(days=today.weekday())

        end_of_week = start_of_week + timedelta(days=6)

        start_of_week_str = start_of_week.strftime("%Y-%m-%d")

        end_of_week_str = end_of_week.strftime("%Y-%m-%d")

        workers_without_second_review = session.exec(
            select(Workers)
            .where(Workers.subsidiarie_id == subsidiarie_id)
            .where(Workers.second_review_date >= start_of_week_str)
            .where(Workers.second_review_date <= end_of_week_str)
            .where(
                ~Workers.id.in_(
                    select(WorkersSecondReview.worker_id).where(
                        WorkersSecondReview.worker_id == Workers.id
                    )
                )
            )
        ).all()

        return {
            "workers": workers_without_second_review,
            "start_of_week": start_of_week,
            "end_of_week": end_of_week,
        }


@app.get("/subsidiaries/{subsidiarie_id}/workers/{worker_id}")
def sla(subsidiarie_id: int, worker_id: int):
    today = datetime.today().date()

    with Session(engine) as session:
        first_review = session.exec(
            select(Workers)
            .where(Workers.subsidiarie_id == subsidiarie_id)
            .where(Workers.id == worker_id)
            .where(Workers.first_review_date >= today)
        ).first()

        can_open_first_review_modal = (
            True
            if session.exec(
                select(Workers)
                .where(Workers.subsidiarie_id == subsidiarie_id)
                .where(Workers.id == worker_id)
                .where(Workers.first_review_date >= today)
            ).first()
            else False
        )

        second_review = session.exec(
            select(Workers)
            .where(Workers.subsidiarie_id == subsidiarie_id)
            .where(Workers.id == worker_id)
            .where(Workers.second_review_date >= today)
        ).first()

        can_open_second_review_modal = (
            True
            if session.exec(
                select(Workers)
                .where(Workers.subsidiarie_id == subsidiarie_id)
                .where(Workers.id == worker_id)
                .where(Workers.second_review_date >= today)
            ).first()
            else False
        )

        return {
            "first_review": first_review,
            "second_review": second_review,
            "can_open_first_review_modal": can_open_first_review_modal,
            "can_open_second_review_modal": can_open_second_review_modal,
        }


from pydantic import BaseModel


class WorkersFieldsByTurnAndFunctionInput(BaseModel):
    fields: list


@app.post(
    "/subsidiaries/{subsidiarie_id}/workers/functions/{function_id}/turns/{turn_id}"
)
def workers_fields_by_turn_and_function(
    subsidiarie_id: int,
    function_id: int,
    turn_id: int,
    input: WorkersFieldsByTurnAndFunctionInput,
):
    with Session(engine) as session:
        workers = session.exec(
            select(Workers, Function, Turn, CostCenter, Department)
            .join(Function, Workers.function_id == Function.id)
            .join(Turn, Workers.turn_id == Turn.id)
            .join(CostCenter, Workers.cost_center_id == CostCenter.id)
            .join(Department, Workers.department_id == Department.id)
            .where(Workers.subsidiarie_id == subsidiarie_id)
            .where(Workers.function_id == function_id)
            .where(Workers.turn_id == turn_id)
        ).all()

        result = [
            {
                "esocial": worker.esocial,
                "enrolment": worker.enrolment,
                "sales_code": worker.sales_code,
                "timecode": worker.timecode,
                "worker_name": worker.name,
                "function_name": function.name,
                "turn_name": turn.name,
                "cost_center_name": cost_center.name,
                "department_name": department.name,
                "admission_date": worker.admission_date,
            }
            for worker, function, turn, cost_center, department in workers
        ]

        return result

        # if not workers:
        #     return []

        # valid_fields = {column.name for column in Workers.__table__.columns}

        # requested_fields = [field for field in input.fields if field in valid_fields]

        # result = [
        #     {field: getattr(worker, field) for field in requested_fields}
        #     for worker in workers
        # ]

        # return workers


from datetime import date


@app.get("/subsidiaries/{id}/get-nr20-list")
def get_nr_list_by_subsidiarie(id: int):
    today = date.today()

    first_day = today.replace(day=1)

    last_day = today.replace(day=1).replace(month=today.month + 1) - timedelta(days=1)

    with Session(engine) as session:
        nr_list = session.exec(
            select(Workers)
            .where(Workers.subsidiarie_id == id)
            .where(Workers.second_review_date.between(first_day, last_day))
        ).all()

        return {"nr_list": nr_list, "first_day": first_day, "last_day": last_day}


# dates events


@app.get(
    "/subsidiaries/{subsidiarie_id}/dates-events", dependencies=[Depends(verify_token)]
)
def get_dates_events(subsidiarie_id: int):
    return handle_get_dates_events(subsidiarie_id)


@app.get(
    "/subsidiaries/{subsidiarie_id}/dates/{date}/dates-events",
    dependencies=[Depends(verify_token)],
)
def get_events_by_date(subsidiarie_id: int, date: str):
    return handle_get_events_by_date(subsidiarie_id, date)


@app.post("/subsidiaries/{id}/dates-events", dependencies=[Depends(verify_token)])
def post_date_event(id: int, date_event: DatesEvents):
    return handle_post_dates_events(id, date_event)


@app.delete(
    "/subsidiaries/{subsidiarie_id}/dates-events/{event_id}",
    dependencies=[Depends(verify_token)],
)
def delete_date_event(subsidiarie_id: int, event_id: int):
    return handle_delete_dates_events(subsidiarie_id, event_id)


# genders


@app.get("/genders")
def get_genders():
    with Session(engine) as session:
        genders = session.exec(select(Genders)).all()

        return genders


# civil status


@app.get("/civil-status")
def get_civil_status():
    with Session(engine) as session:
        civil_status = session.exec(select(CivilStatus)).all()

        return civil_status


@app.get("/ethnicities")
def get_ethnicities():
    with Session(engine) as session:
        ethnicities = session.exec(select(Ethnicity)).all()

        return ethnicities


@app.get("/get-nr-workers")
def get_nr_workers():
    with Session(engine) as session:
        nr_workers = session.exec(select(Workers).where(Workers.second_review_date))


# away reasons


@app.get("/away-reasons")
def get_away_reasons():
    with Session(engine) as session:
        get_away_reasons = select(AwayReasons)

        away_reasons = session.exec(get_away_reasons).all()

        return away_reasons


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


@app.get("/subsidiaries/{id}/hollidays-scale/{date}")
def get_hollidays_scale(id: int, date: str):
    return handle_get_hollidays_scale(id, date)


@app.post("/hollidays-scale")
def post_hollidays_scale(holliday_scale: HollidaysScale):
    return handle_post_hollidays_scale(holliday_scale)


@app.delete("/hollidays-scale/{id}")
def delete_hollidays_scale(id: int):
    return handle_delete_hollidays_scale(id)


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


@app.get("/test-worker")
def test_worker():
    with Session(engine) as session:
        workers = session.exec(select(Workers)).all()

        return workers


# nationalities


@app.get("/nationalities", dependencies=[Depends(verify_token)])
def get_nationalities():
    return handle_get_nationalities()


@app.post("/nationalities", dependencies=[Depends(verify_token)])
def post_nationalities(nationalitie: Nationalities):
    return handle_post_nationalities(nationalitie)


@app.put("/nationalities/{id}", dependencies=[Depends(verify_token)])
def put_nationalities(id: int, nationalitie: Nationalities):
    return handle_put_nationalities(id, nationalitie)


@app.delete("/nationalities/{id}", dependencies=[Depends(verify_token)])
def delete_nationalities(id: int):
    return handle_delete_nationalities(id)


# states


@app.get("/states", dependencies=[Depends(verify_token)])
def get_states():
    return handle_get_states()


@app.get("/states/{id}", dependencies=[Depends(verify_token)])
def get_states_by_id(id: int):
    return handle_get_states_by_id(id)


@app.get("/nationalities/{id}/states", dependencies=[Depends(verify_token)])
def get_states_by_nationalitie(id: int):
    return handle_get_states_by_nationalitie(id)


@app.post("/states", dependencies=[Depends(verify_token)])
def post_states(state: States):
    return handle_post_states(state)


@app.put("/states/{id}", dependencies=[Depends(verify_token)])
def put_states(id: int, state: States):
    return handle_put_states(id, state)


@app.delete("/states/{id}")
def delete_states(id: int):
    return handle_delete_states(id)


# cities


@app.get("/cities")
def get_cities():
    with Session(engine) as session:
        cities = (
            session.exec(
                select(Cities, States).join(States, Cities.state_id == States.id)
            )
            .mappings()
            .all()
        )

        return cities


# @app.get("/cities", dependencies=[Depends(verify_token)])
# @error_handler
# def get_cities():
#     with Session(engine) as session:
#         cities = session.exec(select(Cities)).all()

#         return cities


@app.get("/states/{id}/cities")
def get_cities_by_state(id: int):
    with Session(engine) as session:
        cities = session.exec(select(Cities).where(Cities.state_id == id)).all()

        return cities


@app.get("/cities/{id}", dependencies=[Depends(verify_token)])
@error_handler
def get_city_by_id(id: int):
    with Session(engine) as session:
        cities = session.exec(select(Cities).where(Cities.id == id)).first()

        return cities


async def get_state_by_city_name(city_name: str) -> str:
    # Tenta encontrar no Brasil (via IBGE)
    ibge_url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"

    async with httpx.AsyncClient() as client:
        ibge_response = await client.get(ibge_url)

    if ibge_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro ao acessar a API do IBGE")

    cities_data = ibge_response.json()

    for city in cities_data:
        if city["nome"].lower() == city_name.lower():
            return city["microrregiao"]["mesorregiao"]["UF"]["sigla"]

    # Se não encontrar no IBGE, tenta via Nominatim (OpenStreetMap)
    nominatim_url = (
        f"https://nominatim.openstreetmap.org/search"
        f"?q={city_name},Venezuela&format=json&addressdetails=1&limit=1"
    )

    headers = {"User-Agent": "MyApp/1.0 (meuemail@example.com)"}

    async with httpx.AsyncClient() as client:
        osm_response = await client.get(nominatim_url, headers=headers)

    if osm_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro ao acessar a API Nominatim")

    data = osm_response.json()
    if not data:
        raise HTTPException(
            status_code=404, detail="Cidade não encontrada no Brasil nem na Venezuela"
        )

    address = data[0].get("address", {})
    state = address.get("state") or address.get("region")

    if not state:
        raise HTTPException(
            status_code=500, detail="Estado não encontrado na resposta da API"
        )

    return state


class PostCitiesInput(BaseModel):
    name: str


@app.post("/cities")
async def post_cities(city: PostCitiesInput):
    with Session(engine) as session:
        result = await get_state_by_city_name(city.name)

        new_city_state_id = session.exec(
            select(States.id).where(States.sail == result)
        ).first()

        new_city = Cities(name=city.name, state_id=new_city_state_id)

        session.add(new_city)

        session.commit()

        session.refresh(new_city)

        cities_list = session.exec(select(Cities)).all()

        return cities_list


@app.post("/new-city")
def post_new_city(city: Cities):
    with Session(engine) as session:
        session.add(city)

        session.commit()

        session.refresh(city)

        return city


@app.put("/cities/{id}")
def put_cities(id: int, city: Cities):
    with Session(engine) as session:
        db_city = session.exec(select(Cities).where(Cities.id == id)).first()

        db_city.name = city.name if city.name else db_city.name

        db_city.state_id = city.state_id if city.state_id else db_city.state_id

        session.add(db_city)

        session.commit()

        session.refresh(db_city)

        return db_city


@app.delete("/cities/{id}")
def delete_cities(id: int):
    with Session(engine) as session:
        db_city = session.exec(select(Cities).where(Cities.id == id)).first()

        session.delete(db_city)

        session.commit()

        return {"success": True}


# neighborhoods


@app.get("/neighborhoods")
def get_neighborhoods():
    with Session(engine) as session:
        neighborhoods = session.exec(select(Neighborhoods)).all()

        return neighborhoods


@app.get("/neighborhoods/{id}")
def get_neighborhood_by_id(id: int):
    with Session(engine) as session:
        neighborhood = session.get(Neighborhoods, id)

        return neighborhood


@app.get("/cities/{id}/neighborhoods")
def get_neighborhoods_by_city(id: int):
    with Session(engine) as session:
        neighborhoods = session.exec(
            select(Neighborhoods).where(Neighborhoods.city_id == id)
        ).all()

        return neighborhoods


@app.post("/neighborhoods")
def post_neighborhood(neighborhood: Neighborhoods):
    with Session(engine) as session:
        session.add(neighborhood)

        session.commit()

        session.refresh(neighborhood)

        return neighborhood


def get_city_by_neighborhood(bairro: str) -> str:
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": f"{bairro}, Brasil",
        "format": "json",
        "addressdetails": 1,
        "limit": 1,
    }

    headers = {"User-Agent": "MinhaAplicacao/1.0"}

    response = requests.get(url, params=params, headers=headers)

    data = response.json()

    if not data:
        return "Cidade não encontrada"

    address = data[0].get("address", {})

    return (
        address.get("city")
        or address.get("town")
        or address.get("village", "Cidade não identificada")
    )


class PostNeighborhoodsInput(BaseModel):
    name: str


@app.post("/news")
def post_cities(neighborhood: PostNeighborhoodsInput):
    with Session(engine) as session:
        new_neighborhood_city_name = get_city_by_neighborhood(neighborhood.name)

        new_neighborhood_city_id = session.exec(
            select(Cities.id).where(Cities.name == new_neighborhood_city_name)
        ).first()

        new_neighborhood = Neighborhoods(
            name=neighborhood.name, city_id=new_neighborhood_city_id
        )

        session.add(new_neighborhood)

        session.commit()

        session.refresh(new_neighborhood)

        all_neighborhoods = session.exec(select(Neighborhoods)).all()

        return all_neighborhoods


@app.put("/neighborhoods/{id}")
def put_neighborhood(id: int, neighborhood: Neighborhoods):
    with Session(engine) as session:
        db_neighborhood = session.exec(
            select(Neighborhoods).where(Neighborhoods.id == id)
        ).one()

        if neighborhood is not None and neighborhood.name != db_neighborhood.name:
            db_neighborhood.name = neighborhood.name

        session.add(db_neighborhood)

        session.commit()

        session.refresh(db_neighborhood)

        return db_neighborhood


@app.delete("/neighborhoods/{neighborhood_id}")
def delete_neighborhood(neighborhood_id: int):
    with Session(engine) as session:
        neighborhood = session.get(Neighborhoods, neighborhood_id)

        session.delete(neighborhood)

        session.commit()

        return {"message": "Neighborhood deleted successfully"}


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


@app.get("/get-pdf/{doc_id}")
def get_pdf(doc_id: int):
    try:
        with Session(engine) as session:
            doc = session.get(WorkersDocs, doc_id)
            if not doc:
                raise HTTPException(status_code=404, detail="Documento não encontrado")

            from io import BytesIO

            from fastapi.responses import StreamingResponse

            return StreamingResponse(
                BytesIO(doc.doc),
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f"inline; filename=document_{doc_id}.pdf"
                },
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao recuperar PDF: {str(e)}")


@app.post("/upload-pdf/{worker_id}")
async def upload_pdf(
    worker_id: int,
    doc_title: str = Form(...),  # Novo parâmetro
    file: UploadFile = File(...),
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="O arquivo deve ser um PDF")

    try:
        pdf_bytes = await file.read()

        with Session(engine) as session:
            db_doc = WorkersDocs(
                worker_id=worker_id,
                doc=pdf_bytes,
                doc_title=doc_title,  # Adicionando o título
            )

            session.add(db_doc)
            session.commit()
            session.refresh(db_doc)

            return {
                "message": "PDF salvo com sucesso",
                "id": db_doc.id,
                "worker_id": db_doc.worker_id,
                "doc_title": db_doc.doc_title,  # Retornando o título
                "filename": file.filename,
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar o PDF: {str(e)}")


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

            for page_num in [0, 5]:
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
                filename="Contrato_paginas_1_e_6.pdf",
            )

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_REMETENTE, SENHA)

                smtp.send_message(msg)

            return {"message": "E-mail enviado com sucesso com as páginas 1 e 6"}

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
