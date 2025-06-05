from fastapi import APIRouter, Depends

from controllers.system_log import handle_get_system_log
from functions.auth import verify_token

system_log_routes = APIRouter(dependencies=[Depends(verify_token)])


@system_log_routes.get("/system-log")
def get_system_log():
    return handle_get_system_log()
