from fastapi import APIRouter

from controllers.parents_type import handle_get_parents_type

parents_type_routes = APIRouter()


@parents_type_routes.get("/parents-type")
def get_parents_type():
    return handle_get_parents_type()
