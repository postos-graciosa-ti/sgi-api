from fastapi import APIRouter, Depends

from controllers.turn import (
    handle_get_subsidiarie_turns,
    handle_get_turn_by_id,
    handle_get_turns,
)
from functions.auth import verify_token

turns_routes = APIRouter()


@turns_routes.get("/subsidiaries/{id}/turns", dependencies=[Depends(verify_token)])
def get_subsidiarie_turns(id: int):
    return handle_get_subsidiarie_turns(id)


@turns_routes.get("/turns", dependencies=[Depends(verify_token)])
def get_turns():
    return handle_get_turns()


@turns_routes.get("/turns/{id}", dependencies=[Depends(verify_token)])
def get_turn_by_id(id: int):
    return handle_get_turn_by_id(id)
