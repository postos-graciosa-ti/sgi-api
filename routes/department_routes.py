from fastapi import APIRouter, Depends, Request

from controllers.departments import (
    handle_delete_department,
    handle_get_department_by_id,
    handle_get_departments,
    handle_post_department,
    handle_put_department,
)
from functions.auth import AuthUser, verify_token
from models.department import Department

department_routes = APIRouter(dependencies=[Depends(verify_token)])


@department_routes.get("/departments")
def get_departments():
    return handle_get_departments()


@department_routes.get("/departments/{id}")
def get_department_by_id(id: int):
    return handle_get_department_by_id(id)


@department_routes.post("/departments")
def post_department(
    request: Request,
    department_input: Department,
    user: AuthUser = Depends(verify_token),
):
    return handle_post_department(request, department_input, user)


@department_routes.put("/departments/{id}")
def put_department(
    request: Request,
    id: int,
    department_input: Department,
    user: AuthUser = Depends(verify_token),
):
    return handle_put_department(request, id, department_input, user)


@department_routes.delete("/departments/{id}")
def delete_department(
    request: Request, id: int, user: AuthUser = Depends(verify_token)
):
    return handle_delete_department(request, id, user)
