from fastapi import APIRouter, Depends, Request

from controllers.workers import (
    handle_away_return,
    handle_deactivate_worker,
    handle_delete_worker_notation,
    handle_export_single_worker_excel,
    handle_get_active_workers_by_subsidiarie_and_function,
    handle_get_active_workers_by_turn_and_subsidiarie,
    handle_get_month_birthdays,
    handle_get_worker_by_id,
    handle_get_worker_notations,
    handle_get_workers_approaching_two_years,
    handle_get_workers_by_functions,
    handle_get_workers_by_subsidiarie,
    handle_get_workers_by_subsidiaries_functions_and_turns,
    handle_get_workers_by_turn,
    handle_get_workers_by_turn_and_function,
    handle_get_workers_by_turn_and_subsidiarie,
    handle_get_workers_need_open_account,
    handle_get_workers_need_vt,
    handle_patch_worker_subsidiarie,
    handle_patch_workers_turn,
    handle_post_request_workers_badges,
    handle_post_worker,
    handle_post_worker_notation,
    handle_put_worker,
    handle_reactivate_worker,
    handle_update_worker_metrics,
    handle_worker_away,
)
from controllers.workers_first_review import (
    handle_get_worker_first_review,
    handle_get_workers_first_review,
    handle_get_workers_without_first_review_in_range,
    handle_post_worker_first_review,
)
from controllers.workers_metrics import (
    handle_get_workers_metrics_by_id,
    handle_post_workers_metrics,
)
from controllers.workers_pictures import (
    handle_delete_workers_pictures,
    handle_get_workers_pictures,
    handle_post_workers_pictures,
)
from controllers.workers_second_review import (
    handle_get_worker_second_review,
    handle_get_workers_second_review,
    handle_get_workers_without_second_review_in_range,
    handle_post_worker_second_review,
)
from functions.auth import AuthUser, verify_token
from models.workers import (
    GetWorkersVtReportBody,
    MetricsUpdateRequest,
    PatchWorkersTurnBody,
    RequestBadgesBody,
    WorkerDeactivateInput,
    Workers,
    WorkersAway,
)
from models.workers_first_review import WorkersFirstReview
from models.workers_metrics import WorkersMetrics
from models.workers_pictures import WorkersPictures
from models.workers_second_review import WorkersSecondReview
from pyhints.workers import PostWorkerNotationInput

workers_routes = APIRouter(dependencies=[Depends(verify_token)])


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


@workers_routes.get(
    "/user-subsidiaries/{user_id}/workers/enterprise-two-year-anniversary"
)
def get_workers_approaching_two_years(user_id: int):
    handle_get_workers_approaching_two_years(user_id)


@workers_routes.get(
    "/subsidiaries/{subsidiarie_id}/workers/functions/{function_id}/turns/{turn_id}"
)
def get_workers_by_functions(subsidiarie_id: int, function_id: int, turn_id: int):
    return handle_get_workers_by_functions(subsidiarie_id, function_id, turn_id)


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


@workers_routes.put("/subsidiaries/{subsidiarie_id}/workers/{worker_id}/away")
def worker_away(subsidiarie_id: int, worker_id: int, worker: WorkersAway):
    return handle_worker_away(subsidiarie_id, worker_id, worker)


@workers_routes.put("/subsidiaries/{subsidiarie_id}/workers/{worker_id}/away-return")
def away_return(subsidiarie_id: int, worker_id: int):
    return handle_away_return(subsidiarie_id, worker_id)


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


@workers_routes.post("/workers/request-badges")
def post_request_workers_badges(body: RequestBadgesBody):
    return handle_post_request_workers_badges(body)


@workers_routes.get("/workers-pictures/{worker_id}")
def get_workers_pictures(worker_id: int):
    return handle_get_workers_pictures(worker_id)


@workers_routes.post("/workers-pictures")
def post_workers_pictures(body: WorkersPictures):
    return handle_post_workers_pictures(body)


@workers_routes.delete("/workers-pictures/{worker_id}")
def delete_workers_pictures(worker_id: int):
    return handle_delete_workers_pictures(worker_id)


@workers_routes.get(
    "/subsidiaries/{subsidiarie_id}/workers/experience-time-no-first-review"
)
def get_workers_without_first_review_in_range(subsidiarie_id: int):
    return handle_get_workers_without_first_review_in_range(subsidiarie_id)


@workers_routes.get("/workers/{id}/first-review")
def get_worker_first_review(id: int):
    return handle_get_worker_first_review(id)


@workers_routes.post("/workers/{id}/first-review")
def post_worker_first_review(id: int, worker_first_review: WorkersFirstReview):
    return handle_post_worker_first_review(id, worker_first_review)


@workers_routes.get("/subsidiaries/{subsidiarie_id}/workers/first-review/notification")
def get_workers_first_review(subsidiarie_id: int):
    return handle_get_workers_first_review(subsidiarie_id)


@workers_routes.get(
    "/subsidiaries/{subsidiarie_id}/workers/experience-time-no-second-review"
)
def get_workers_without_second_review_in_range(subsidiarie_id: int):
    return handle_get_workers_without_second_review_in_range(subsidiarie_id)


@workers_routes.get("/workers/{id}/second-review")
def get_worker_second_review(id: int):
    return handle_get_worker_second_review(id)


@workers_routes.post("/workers/{id}/second-review")
def post_worker_second_review(id: int, worker_second_review: WorkersSecondReview):
    return handle_post_worker_second_review(id, worker_second_review)


@workers_routes.get("/subsidiaries/{subsidiarie_id}/workers/second-review/notification")
def get_workers_second_review(subsidiarie_id: int):
    return handle_get_workers_second_review(subsidiarie_id)


@workers_routes.get("/workers-metrics/{id}")
def get_workers_metrics_by_id(id: int):
    return handle_get_workers_metrics_by_id(id)


@workers_routes.post("/workers-metrics")
def post_workers_metrics(workers_metrics: WorkersMetrics):
    return handle_post_workers_metrics(workers_metrics)


@workers_routes.patch("/workers-metrics/{metrics_id}")
def update_worker_metrics(metrics_id: int, body: MetricsUpdateRequest):
    return handle_update_worker_metrics(metrics_id, body)
