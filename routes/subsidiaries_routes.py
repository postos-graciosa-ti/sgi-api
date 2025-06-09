from fastapi import APIRouter, Depends, Request

from controllers.subsidiaries import (
    handle_delete_subsidiarie,
    handle_get_subsidiarie_by_id,
    handle_get_subsidiaries,
    handle_post_subsidiaries,
    handle_put_subsidiarie,
)
from controllers.subsidiaries_notifications import (
    handle_get_subsidiarie_notifications,
    handle_get_subsidiaries_status,
)
from functions.auth import AuthUser, verify_token
from models.subsidiarie import Subsidiarie

subsidiaries_routes = APIRouter()


@subsidiaries_routes.get("/subsidiaries", dependencies=[Depends(verify_token)])
def get_subsidiaries():
    return handle_get_subsidiaries()


@subsidiaries_routes.get("/subsidiaries/{id}", dependencies=[Depends(verify_token)])
def get_subsidiarie_by_id(id: int):
    return handle_get_subsidiarie_by_id(id)


@subsidiaries_routes.post("/subsidiaries")
def post_subsidiaries(
    request: Request, formData: Subsidiarie, user: AuthUser = Depends(verify_token)
):
    return handle_post_subsidiaries(request, formData, user)


@subsidiaries_routes.put("/subsidiaries/{id}")
def put_subsidiarie(
    id: int,
    formData: Subsidiarie,
    request: Request,
    user: AuthUser = Depends(verify_token),
):
    return handle_put_subsidiarie(id, formData, request, user)


@subsidiaries_routes.delete("/subsidiaries/{id}")
def delete_subsidiaries(
    request: Request,
    id: int,
    user: AuthUser = Depends(verify_token),
):
    return handle_delete_subsidiarie(request, id, user)


@subsidiaries_routes.get(
    "/subsidiaries/{id}/notifications", dependencies=[Depends(verify_token)]
)
async def get_subsidiarie_notifications(id: int):
    return await handle_get_subsidiarie_notifications(id)


@subsidiaries_routes.get(
    "/subsidiaries/{id}/workers-status", dependencies=[Depends(verify_token)]
)
def get_subsidiaries_status(id: int):
    return handle_get_subsidiaries_status(id)
