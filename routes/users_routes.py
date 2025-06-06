from fastapi import APIRouter, Depends, Request

from controllers.users import (
    handle_change_password,
    handle_confirm_password,
    handle_delete_user,
    handle_get_test,
    handle_get_user_by_id,
    handle_get_users,
    handle_get_users_by_status,
    handle_get_users_roles,
    handle_patch_deactivate_user,
    handle_post_user,
    handle_put_user,
)
from functions.auth import AuthUser, verify_token
from models.user import User
from pyhints.users import ChangeUserPasswordInput, ConfirmPassword, Test

users_routes = APIRouter()


@users_routes.get("/users", dependencies=[Depends(verify_token)])
def get_users():
    return handle_get_users()


@users_routes.get("/users/{id}", dependencies=[Depends(verify_token)])
def get_user_by_id(id: int):
    return handle_get_user_by_id(id)


@users_routes.get("/users_roles", dependencies=[Depends(verify_token)])
def get_users_roles():
    return handle_get_users_roles()


@users_routes.get("/users/status/{status}", dependencies=[Depends(verify_token)])
def get_users_by_status(status: str):
    return handle_get_users_by_status(status)


@users_routes.post("/users")
def post_user(
    request: Request, user: User, loged_user: AuthUser = Depends(verify_token)
):
    return handle_post_user(request, user, loged_user)


@users_routes.put("/users/{id}")
def put_user(
    request: Request, id: int, user: User, loged_user: AuthUser = Depends(verify_token)
):
    return handle_put_user(request, id, user, loged_user)


@users_routes.patch("/users/{id}/created_by/{created_by_id}/deactivate")
def patch_deactivate_user(
    request: Request,
    id: int,
    created_by_id: int,
    loged_user: AuthUser = Depends(verify_token),
):
    return handle_patch_deactivate_user(request, id, created_by_id, loged_user)


@users_routes.delete("/users/{id}", dependencies=[Depends(verify_token)])
def delete_user(id: int):
    return handle_delete_user(id)


@users_routes.post("/test", dependencies=[Depends(verify_token)])
def test(arr: Test):
    return handle_get_test(arr)


@users_routes.post("/confirm-password", dependencies=[Depends(verify_token)])
def confirm_password(userData: ConfirmPassword):
    return handle_confirm_password(userData)


@users_routes.post("/users/change-password", dependencies=[Depends(verify_token)])
def change_password(userData: ChangeUserPasswordInput):
    return handle_change_password(userData)
