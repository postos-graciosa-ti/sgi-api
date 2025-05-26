from fastapi import APIRouter

from controllers.open_positions import (
    handle_delete_open_positions,
    handle_get_open_positions,
    handle_get_open_positions_by_subsidiarie,
    handle_post_open_positions,
)
from models.open_positions import OpenPositions

routes = APIRouter()


@routes.get("/open-positions")
def get_open_positions():
    return handle_get_open_positions()


@routes.get("/subsidiaries/{id}/open-positions")
def get_open_positions_by_subsidiarie(id: int):
    return handle_get_open_positions_by_subsidiarie(id)


@routes.post("/open-positions")
def post_open_positions(open_position: OpenPositions):
    return handle_post_open_positions(open_position)


@routes.delete("/open-positions/{id}")
def delete_open_positions(id: int):
    return handle_delete_open_positions(id)
