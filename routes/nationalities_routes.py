from fastapi import APIRouter, Depends

from controllers.nationalities import (
    handle_delete_nationalities,
    handle_get_nationalities,
    handle_post_nationalities,
    handle_put_nationalities,
)
from functions.auth import AuthUser, verify_token
from models.nationalities import Nationalities

nationalities_routes = APIRouter()


@nationalities_routes.get("/nationalities", dependencies=[Depends(verify_token)])
def get_nationalities():
    return handle_get_nationalities()


@nationalities_routes.post("/nationalities")
def post_nationalities(
    nationality: Nationalities, user: AuthUser = Depends(verify_token)
):
    return handle_post_nationalities(nationality, user)


@nationalities_routes.put("/nationalities/{id}")
def put_nationalities(
    id: int, nationality: Nationalities, user: AuthUser = Depends(verify_token)
):
    return handle_put_nationalities(id, nationality, user)


@nationalities_routes.delete("/nationalities/{id}")
def delete_nationalities(id: int, user: AuthUser = Depends(verify_token)):
    return handle_delete_nationalities(id, user)
