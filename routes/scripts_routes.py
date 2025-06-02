from typing import Annotated

from fastapi import APIRouter, File, Form, UploadFile

from scripts.excel_scraping import handle_excel_scraping
from scripts.rh_sheets import handle_post_scripts_rhsheets
from scripts.sync_workers_data import handle_post_sync_workers_data

scripts_routes = APIRouter()


@scripts_routes.post("/subsidiaries/{id}/scripts/excel-scraping")
async def excel_scraping(id: int, file: UploadFile = File(...)):
    return await handle_excel_scraping(id, file)


@scripts_routes.post("/scripts/rhsheets")
async def post_scripts_rhsheets(
    discountList: Annotated[str, Form()], file: UploadFile = File(...)
):
    return await handle_post_scripts_rhsheets(discountList, file)


@scripts_routes.post("/scripts/sync-workers-data")
def post_sync_workers_data(file: UploadFile = File(...)):
    return handle_post_sync_workers_data(file)
