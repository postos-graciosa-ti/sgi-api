from fastapi import APIRouter

from controllers.ethnicities import handle_get_ethnicities

ethnicities_routes = APIRouter()


@ethnicities_routes.get("/ethnicities")
def get_ethnicities():
    return handle_get_ethnicities()
