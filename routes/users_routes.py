from fastapi import APIRouter, Depends

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
from functions.auth import verify_token
from models.user import User
from pyhints.users import ChangeUserPasswordInput, ConfirmPassword, Test

users_routes = APIRouter(dependencies=[Depends(verify_token)])


@users_routes.get("/users")
def get_users():
    return handle_get_users()


@users_routes.get("/users/{id}")
def get_user_by_id(id: int):
    return handle_get_user_by_id(id)


@users_routes.get("/users_roles")
def get_users_roles():
    return handle_get_users_roles()


@users_routes.get("/users/status/{status}")
def get_users_by_status(status: str):
    return handle_get_users_by_status(status)


@users_routes.post("/users")
def post_user(user: User):
    return handle_post_user(user)


@users_routes.put("/users/{id}")
def put_user(id: int, user: User):
    return handle_put_user(id, user)


@users_routes.patch("/users/{id}/created_by/{created_by_id}/deactivate")
def patch_deactivate_user(id: int, created_by_id: int):
    return handle_patch_deactivate_user(id, created_by_id)


@users_routes.delete("/users/{id}")
def delete_user(id: int):
    return handle_delete_user(id)


@users_routes.post("/test")
def test(arr: Test):
    return handle_get_test(arr)


@users_routes.post("/confirm-password")
def confirm_password(userData: ConfirmPassword):
    return handle_confirm_password(userData)


@users_routes.post("/users/change-password")
def change_password(userData: ChangeUserPasswordInput):
    return handle_change_password(userData)
