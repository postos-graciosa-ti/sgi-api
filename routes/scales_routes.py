from fastapi import APIRouter, Depends

from controllers.scale import (
    handle_delete_scale,
    handle_get_days_off_quantity,
    handle_get_scales_by_subsidiarie_and_worker_id,
    handle_get_scales_by_subsidiarie_id,
    handle_get_scales_logs,
    handle_handle_scale,
    handle_post_scale,
    handle_post_scales_logs,
    handle_post_some_workers_scale,
    handle_post_subsidiarie_scale_to_print,
)
from controllers.scales_reports import (
    handle_generate_scale_days_off_report,
    handle_generate_scale_days_on_report,
)
from functions.auth import verify_token
from models.scale_logs import ScaleLogs
from pyhints.scales import (
    PostScaleInput,
    PostSomeWorkersScaleInput,
    ScalesPrintInput,
    ScalesReportInput,
    WorkerDeactivateInput,
)

scales_routes = APIRouter(dependencies=[Depends(verify_token)])


@scales_routes.get(
    "/scales/subsidiaries/{subsidiarie_id}",
)
def get_scales_by_subsidiarie_id(subsidiarie_id: int):
    return handle_get_scales_by_subsidiarie_id(subsidiarie_id)


@scales_routes.get("/scales/subsidiaries/{subsidiarie_id}/workers/{worker_id}")
def get_scales_by_subsidiarie_and_worker_id(subsidiarie_id: int, worker_id: int):
    return handle_get_scales_by_subsidiarie_and_worker_id(subsidiarie_id, worker_id)


@scales_routes.get("/scales/day-off/quantity")
def get_days_off_quantity():
    return handle_get_days_off_quantity()


@scales_routes.post("/scales")
def post_scale(form_data: PostScaleInput):
    return handle_post_scale(form_data)


@scales_routes.post("/scales/some-workers")
def post_some_workers_scale(form_data: PostSomeWorkersScaleInput):
    return handle_post_some_workers_scale(form_data)


@scales_routes.post("/delete-scale")
def handle_scale(form_data: PostScaleInput):
    return handle_handle_scale(form_data)


@scales_routes.delete("/scales/{scale_id}/subsidiaries/{subsidiarie_id}")
def delete_scale(scale_id: int, subsidiarie_id: int):
    return handle_delete_scale(scale_id, subsidiarie_id)


@scales_routes.get("/subsidiaries/{id}/scales/logs")
def get_scales_logs(id: int):
    return handle_get_scales_logs(id)


@scales_routes.post("/subsidiaries/{id}/scales/logs")
def post_scales_logs(id: int, scale_log: ScaleLogs):
    return handle_post_scales_logs(id, scale_log)


@scales_routes.post("/reports/subsidiaries/{subsidiarie_id}/scales/days-on")
async def generate_scale_days_on_report(subsidiarie_id: int, input: ScalesReportInput):
    return await handle_generate_scale_days_on_report(subsidiarie_id, input)


@scales_routes.post("/reports/subsidiaries/{subsidiarie_id}/scales/days-off")
async def generate_scale_days_off_report(subsidiarie_id: int, input: ScalesReportInput):
    return await handle_generate_scale_days_off_report(subsidiarie_id, input)


@scales_routes.post("/subsidiaries/{id}/scales/print")
def post_subsidiarie_scale_to_print(id: int, scales_print_input: ScalesPrintInput):
    return handle_post_subsidiarie_scale_to_print(id, scales_print_input)
