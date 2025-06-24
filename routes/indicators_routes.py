from fastapi import APIRouter

from controllers.indicators import handle_get_indicators, handle_post_indicators
from models.indicators import Indicators

indicators_routes = APIRouter()


@indicators_routes.get("/indicators")
def get_indicators():
    return handle_get_indicators()


@indicators_routes.post("/indicators")
def post_indicators(indicator: Indicators):
    return handle_post_indicators(indicator)
