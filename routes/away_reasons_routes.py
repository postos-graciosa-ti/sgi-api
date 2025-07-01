from fastapi import APIRouter

from controllers.away_reasons import handle_get_away_reasons

away_reasons_routes = APIRouter()


@away_reasons_routes.get("/away-reasons")
def get_away_reasons():
    return handle_get_away_reasons()
