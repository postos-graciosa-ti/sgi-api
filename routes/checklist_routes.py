from fastapi import APIRouter, status

from controllers.checklist import (
    handle_create_checklist,
    handle_get_checklist_by_worker,
    handle_patch_checklist,
)
from models.checklist import Checklist, ChecklistCreate, ChecklistUpdate

checklist_routes = APIRouter()


@checklist_routes.get("/checklist/worker/{worker_id}", response_model=Checklist)
def get_checklist_by_worker(worker_id: int):
    return handle_get_checklist_by_worker(worker_id)


@checklist_routes.post(
    "/checklist", status_code=status.HTTP_201_CREATED, response_model=Checklist
)
def create_checklist(checklist: ChecklistCreate):
    return handle_create_checklist(checklist)


@checklist_routes.patch("/checklist/{checklist_id}", response_model=Checklist)
def patch_checklist(checklist_id: int, checklist_update: ChecklistUpdate):
    return handle_patch_checklist(checklist_id, checklist_update)
