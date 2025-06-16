from fastapi import APIRouter, Depends, Request

from controllers.workers import (
    handle_deactivate_worker,
    handle_delete_worker_notation,
    handle_export_single_worker_excel,
    handle_get_active_workers_by_subsidiarie_and_function,
    handle_get_active_workers_by_turn_and_subsidiarie,
    handle_get_month_birthdays,
    handle_get_worker_by_id,
    handle_get_worker_notations,
    handle_get_workers_by_subsidiarie,
    handle_get_workers_by_subsidiaries_functions_and_turns,
    handle_get_workers_by_turn,
    handle_get_workers_by_turn_and_function,
    handle_get_workers_by_turn_and_subsidiarie,
    handle_get_workers_need_open_account,
    handle_get_workers_need_vt,
    handle_patch_worker_subsidiarie,
    handle_patch_workers_turn,
    handle_post_worker,
    handle_post_worker_notation,
    handle_put_worker,
    handle_reactivate_worker,
)
from controllers.workers_pictures import (
    handle_delete_workers_pictures,
    handle_get_workers_pictures,
    handle_post_workers_pictures,
)
from functions.auth import AuthUser, verify_token
from models.workers import (
    GetWorkersVtReportBody,
    PatchWorkersTurnBody,
    WorkerDeactivateInput,
    Workers,
)
from models.workers_pictures import WorkersPictures
from pyhints.workers import PostWorkerNotationInput

workers_routes = APIRouter()


@workers_routes.get("/workers/{id}", dependencies=[Depends(verify_token)])
def get_worker_by_id(id: int):
    return handle_get_worker_by_id(id)


@workers_routes.get(
    "/workers/turns/{turn_id}/subsidiarie/{subsidiarie_id}",
    dependencies=[Depends(verify_token)],
)
def get_workers_by_turn_and_subsidiarie(turn_id: int, subsidiarie_id: int):
    return handle_get_workers_by_turn_and_subsidiarie(turn_id, subsidiarie_id)


@workers_routes.get(
    "/workers/on-track/turn/{turn_id}/subsidiarie/{subsidiarie_id}",
    dependencies=[Depends(verify_token)],
)
def get_active_workers_by_turn_and_subsidiarie(turn_id: int, subsidiarie_id: int):
    return handle_get_active_workers_by_turn_and_subsidiarie(turn_id, subsidiarie_id)


@workers_routes.get(
    "/workers/active/subsidiarie/{subsidiarie_id}/function/{function_id}",
    dependencies=[Depends(verify_token)],
)
def get_active_workers_by_subsidiarie_and_function(
    subsidiarie_id: int, function_id: int
):
    return handle_get_active_workers_by_subsidiarie_and_function(
        subsidiarie_id, function_id
    )


@workers_routes.get(
    "/workers/subsidiarie/{subsidiarie_id}", dependencies=[Depends(verify_token)]
)
def get_workers_by_subsidiarie(subsidiarie_id: int):
    return handle_get_workers_by_subsidiarie(subsidiarie_id)


@workers_routes.get(
    "/workers/subsidiaries/{subsidiarie_id}/functions/{function_id}/turns/{turn_id}",
    dependencies=[Depends(verify_token)],
)
def get_workers_by_subsidiaries_functions_and_turns(
    subsidiarie_id: int, function_id: int, turn_id: int
):
    return handle_get_workers_by_subsidiaries_functions_and_turns(
        subsidiarie_id, function_id, turn_id
    )


@workers_routes.get(
    "/subsidiaries/{subsidiarie_id}/turns/{turn_id}/functions/{function_id}/workers",
    dependencies=[Depends(verify_token)],
)
def get_workers_by_turn_and_function(
    subsidiarie_id: int, turn_id: int, function_id: int
):
    return handle_get_workers_by_turn_and_function(subsidiarie_id, turn_id, function_id)


@workers_routes.get(
    "/subsidiaries/{subsidiarie_id}/turns/{turn_id}/workers",
    dependencies=[Depends(verify_token)],
)
def get_workers_by_turn(subsidiarie_id: int, turn_id: int):
    return handle_get_workers_by_turn(subsidiarie_id, turn_id)


@workers_routes.get("/subsidiaries/{id}/another-route-yet")
def get_month_birthdays(id: int):
    return handle_get_month_birthdays(id)


@workers_routes.get("/export/worker/{worker_id}")
def export_single_worker_excel(worker_id: int):
    return handle_export_single_worker_excel(worker_id)


@workers_routes.post("/workers")
def post_worker(
    request: Request, worker: Workers, user: AuthUser = Depends(verify_token)
):
    return handle_post_worker(request, worker, user)


@workers_routes.post("/workers/vt-report", dependencies=[Depends(verify_token)])
def get_workers_need_vt(body: GetWorkersVtReportBody):
    return handle_get_workers_need_vt(body)


@workers_routes.post(
    "/workers/open-account-report", dependencies=[Depends(verify_token)]
)
def get_workers_need_open_account(body: GetWorkersVtReportBody):
    return handle_get_workers_need_open_account(body)


@workers_routes.put("/workers/{id}")
def put_worker(
    request: Request, id: int, worker: Workers, user: AuthUser = Depends(verify_token)
):
    return handle_put_worker(request, id, worker, user)


@workers_routes.put("/workers/{id}/deactivate")
def deactivate_worker(
    request: Request,
    id: int,
    worker: WorkerDeactivateInput,
    user: AuthUser = Depends(verify_token),
):
    return handle_deactivate_worker(request, id, worker, user)


@workers_routes.put("/workers/{id}/reactivate")
def reactivate_worker(
    request: Request, id: int, user: AuthUser = Depends(verify_token)
):
    return handle_reactivate_worker(request, id, user)


@workers_routes.patch("/patch-workers-turn", dependencies=[Depends(verify_token)])
def patch_workers_turn(body: PatchWorkersTurnBody):
    return handle_patch_workers_turn(body)


@workers_routes.patch("/workers/{worker_id}/change-subsidiarie/{subsidiarie_id}")
def patch_worker_subsidiarie(worker_id: int, subsidiarie_id: int):
    return handle_patch_worker_subsidiarie(worker_id, subsidiarie_id)


@workers_routes.get("/workers/{id}/notations", dependencies=[Depends(verify_token)])
def get_worker_notations(id: int):
    return handle_get_worker_notations(id)


@workers_routes.post("/workers/{id}/notations", dependencies=[Depends(verify_token)])
def post_worker_notation(id: int, data: PostWorkerNotationInput):
    return handle_post_worker_notation(id, data)


@workers_routes.delete("/workers-notations/{id}", dependencies=[Depends(verify_token)])
def delete_worker_notation(id: int):
    return handle_delete_worker_notation(id)


@workers_routes.get("/workers-pictures/{worker_id}")
def get_workers_pictures(worker_id: int):
    return handle_get_workers_pictures(worker_id)


@workers_routes.post("/workers-pictures")
def post_workers_pictures(body: WorkersPictures):
    return handle_post_workers_pictures(body)


@workers_routes.delete("/workers-pictures/{worker_id}")
def delete_workers_pictures(worker_id: int):
    return handle_delete_workers_pictures(worker_id)
