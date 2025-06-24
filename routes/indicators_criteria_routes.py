from fastapi import APIRouter, Depends

from controllers.indicators_criteria import (
    handle_get_indicators_criteria,
    handle_post_indicators_criteria,
)
from functions.auth import verify_token
from models.indicators_criteria import IndicatorsCriteria

indicators_criteria_routes = APIRouter(dependencies=[Depends(verify_token)])


@indicators_criteria_routes.get("/indicators-criteria")
def get_indicators_criteria():
    return handle_get_indicators_criteria()


@indicators_criteria_routes.post("/indicators-criteria")
def post_indicators_criteria(indicator_criteria: IndicatorsCriteria):
    return handle_post_indicators_criteria(indicator_criteria)
