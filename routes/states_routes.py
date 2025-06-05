from fastapi import APIRouter, Depends

from controllers.states import (
    handle_delete_states,
    handle_get_states,
    handle_get_states_by_id,
    handle_get_states_by_nationalitie,
    handle_post_states,
    handle_put_states,
)
from functions.auth import verify_token
from models.states import States

states_routes = APIRouter(dependencies=[Depends(verify_token)])


@states_routes.get("/states")
def get_states():
    return handle_get_states()


@states_routes.get("/states/{id}")
def get_states_by_id(id: int):
    return handle_get_states_by_id(id)


@states_routes.get("/nationalities/{id}/states")
def get_states_by_nationalitie(id: int):
    return handle_get_states_by_nationalitie(id)


@states_routes.post("/states")
def post_states(state: States):
    return handle_post_states(state)


@states_routes.put("/states/{id}")
def put_states(id: int, state: States):
    return handle_put_states(id, state)


@states_routes.delete("/states/{id}")
def delete_states(id: int):
    return handle_delete_states(id)
