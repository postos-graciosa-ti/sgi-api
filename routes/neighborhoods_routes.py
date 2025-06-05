from fastapi import APIRouter, Depends

from controllers.neighborhoods import (
    handle_delete_neighborhood,
    handle_get_neighborhood_by_id,
    handle_get_neighborhoods,
    handle_get_neighborhoods_by_city,
    handle_post_neighborhood,
    handle_put_neighborhood,
)
from functions.auth import verify_token
from models.neighborhoods import Neighborhoods

neighborhoods_routes = APIRouter(dependencies=[Depends(verify_token)])


@neighborhoods_routes.get("/neighborhoods")
def get_neighborhoods():
    return handle_get_neighborhoods()


@neighborhoods_routes.get("/neighborhoods/{id}")
def get_neighborhood_by_id(id: int):
    return handle_get_neighborhood_by_id(id)


@neighborhoods_routes.get("/cities/{id}/neighborhoods")
def get_neighborhoods_by_city(id: int):
    return handle_get_neighborhoods_by_city(id)


@neighborhoods_routes.post("/neighborhoods")
def post_neighborhood(neighborhood: Neighborhoods):
    return handle_post_neighborhood(neighborhood)


@neighborhoods_routes.put("/neighborhoods/{id}")
def put_neighborhood(id: int, neighborhood: Neighborhoods):
    return handle_put_neighborhood(id, neighborhood)


@neighborhoods_routes.delete("/neighborhoods/{neighborhood_id}")
def delete_neighborhood(neighborhood_id: int):
    return handle_delete_neighborhood(neighborhood_id)
