from fastapi import APIRouter, Depends

from controllers.resignable_reasons import (
    handle_get_resignable_reasons,
    handle_resignable_reasons_report,
)
from functions.auth import verify_token
from pyhints.resignable_reasons import StatusResignableReasonsInput

resignable_reasons_routes = APIRouter()


@resignable_reasons_routes.get(
    "/resignable-reasons", dependencies=[Depends(verify_token)]
)
def get_resignable_reasons():
    return handle_get_resignable_reasons()


@resignable_reasons_routes.post(
    "/subsidiaries/{id}/resignable-reasons/report", dependencies=[Depends(verify_token)]
)
def get_resignable_reasons_report(id: int, input: StatusResignableReasonsInput):
    return handle_resignable_reasons_report(id, input)
