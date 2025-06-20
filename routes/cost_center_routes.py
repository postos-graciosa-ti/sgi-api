from fastapi import APIRouter, Depends, Request

from controllers.cost_center import (
    handle_delete_cost_center,
    handle_get_cost_center,
    handle_get_cost_center_by_id,
    handle_post_cost_center,
    handle_put_cost_center,
)
from functions.auth import AuthUser, verify_token
from models.cost_center import CostCenter

cost_center_routes = APIRouter(dependencies=[Depends(verify_token)])


@cost_center_routes.get("/cost-center")
def get_cost_center():
    return handle_get_cost_center()


@cost_center_routes.get("/cost-center/{id}")
def get_cost_center_by_id(id: int):
    return handle_get_cost_center_by_id(id)


@cost_center_routes.post("/cost-center")
def post_cost_center(
    request: Request,
    cost_center_input: CostCenter,
    user: AuthUser = Depends(verify_token),
):
    return handle_post_cost_center(request, cost_center_input, user)


@cost_center_routes.put("/cost-center/{id}")
def put_cost_center(
    request: Request,
    id: int,
    cost_center_input: CostCenter,
    user: AuthUser = Depends(verify_token),
):
    return handle_put_cost_center(request, id, cost_center_input, user)


@cost_center_routes.delete("/cost-center/{id}")
def delete_cost_center(
    request: Request, id: int, user: AuthUser = Depends(verify_token)
):
    return handle_delete_cost_center(request, id, user)
