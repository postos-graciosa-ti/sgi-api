from fastapi import APIRouter, Depends

from controllers.cities import (
    handle_delete_cities,
    handle_get_cities,
    handle_get_cities_by_state,
    handle_get_city_by_id,
    handle_post_new_city,
    handle_put_cities,
)
from functions.auth import verify_token
from models.cities import Cities

cities_routes = APIRouter(dependencies=[Depends(verify_token)])


@cities_routes.get("/cities")
def get_cities():
    return handle_get_cities()


@cities_routes.get("/cities/{id}")
def get_city_by_id(id: int):
    return handle_get_city_by_id(id)


@cities_routes.get("/states/{id}/cities")
def get_cities_by_state(id: int):
    return handle_get_cities_by_state(id)


@cities_routes.post("/new-city")
def post_new_city(city: Cities):
    return handle_post_new_city(city)


@cities_routes.put("/cities/{id}")
def put_cities(id: int, city: Cities):
    return handle_put_cities(id, city)


@cities_routes.delete("/cities/{id}")
def delete_cities(id: int):
    return handle_delete_cities(id)
