from fastapi import APIRouter, Depends, Request

from controllers.turn import (
    handle_delete_turn,
    handle_get_subsidiarie_turns,
    handle_get_turn_by_id,
    handle_get_turns,
    handle_post_turns,
    handle_put_turn,
)
from functions.auth import AuthUser, verify_token
from models.turn import Turn
from pyhints.turns import PutTurn

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


@turns_routes.post("/turns")
def post_turns(
    request: Request, formData: Turn, user: AuthUser = Depends(verify_token)
):
    return handle_post_turns(request, formData, user)


@turns_routes.put("/turns/{id}")
def put_turn(
    request: Request, id: int, formData: PutTurn, user: AuthUser = Depends(verify_token)
):
    return handle_put_turn(request, id, formData, user)


@turns_routes.delete("/turns/{id}")
def delete_turn(request: Request, id: int, user: AuthUser = Depends(verify_token)):
    return handle_delete_turn(request, id, user)
