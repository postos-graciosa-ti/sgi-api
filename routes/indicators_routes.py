from fastapi import APIRouter

from controllers.indicators import (
    handle_delete_indicators,
    handle_get_indicators,
    handle_get_indicators_by_month_and_criteria,
    handle_post_indicators,
)
from models.indicators import Indicators, PostIndicatorsByMonthAndCriteria

indicators_routes = APIRouter()


@indicators_routes.get("/indicators")
def get_indicators():
    return handle_get_indicators()


@indicators_routes.post("/indicators_by_month_and_criteria")
def get_indicators_by_month_and_criteria(body: PostIndicatorsByMonthAndCriteria):
    return handle_get_indicators_by_month_and_criteria(body)


@indicators_routes.post("/indicators")
def post_indicators(indicator: Indicators):
    return handle_post_indicators(indicator)


@indicators_routes.delete("/indicators/{id}")
def delete_indicators(id: int):
    return handle_delete_indicators(id)
