from fastapi import APIRouter, Depends, Request

from controllers.functions import (
    handle_delete_function,
    handle_get_functions,
    handle_get_functions_by_subsidiarie,
    handle_get_functions_for_users,
    handle_post_function,
    handle_put_function,
)
from functions.auth import AuthUser, verify_token
from models.function import Function

functions_routes = APIRouter(dependencies=[Depends(verify_token)])


@functions_routes.get("/subsidiaries/{id}/functions")
def get_functions_by_subsidiarie(id: int):
    return handle_get_functions_by_subsidiarie(id)


@functions_routes.get("/functions")
def get_functions():
    return handle_get_functions()


@functions_routes.get("/functions/for-users")
def get_functions_for_users():
    return handle_get_functions_for_users()


@functions_routes.post("/functions")
def post_function(
    request: Request, function: Function, user: AuthUser = Depends(verify_token)
):
    return handle_post_function(request, function, user)


@functions_routes.put("/functions/{id}")
def put_function(
    request: Request,
    id: int,
    function: Function,
    user: AuthUser = Depends(verify_token),
):
    return handle_put_function(request, id, function, user)


@functions_routes.delete("/functions/{id}")
def delete_function(
    request: Request,
    id: int,
    user: AuthUser = Depends(verify_token),
):
    return handle_delete_function(request, id, user)
