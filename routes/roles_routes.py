from fastapi import APIRouter, Depends

from controllers.roles import handle_get_roles, handle_get_roles_by_id
from functions.auth import verify_token

roles_routes = APIRouter(dependencies=[Depends(verify_token)])


@roles_routes.get("/roles")
def get_roles():
    return handle_get_roles()


@roles_routes.get("/roles/{id}")
def get_roles_by_id(id: int):
    return handle_get_roles_by_id(id)
