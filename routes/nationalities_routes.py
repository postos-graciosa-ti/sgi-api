from fastapi import APIRouter, Depends

from controllers.nationalities import (
    handle_delete_nationalities,
    handle_get_nationalities,
    handle_post_nationalities,
    handle_put_nationalities,
)
from functions.auth import verify_token
from models.nationalities import Nationalities

nationalities_routes = APIRouter(dependencies=[Depends(verify_token)])


@nationalities_routes.get("/nationalities")
def get_nationalities():
    return handle_get_nationalities()


@nationalities_routes.post("/nationalities")
def post_nationalities(nationalitie: Nationalities):
    return handle_post_nationalities(nationalitie)


@nationalities_routes.put("/nationalities/{id}")
def put_nationalities(id: int, nationalitie: Nationalities):
    return handle_put_nationalities(id, nationalitie)


@nationalities_routes.delete("/nationalities/{id}")
def delete_nationalities(id: int):
    return handle_delete_nationalities(id)
