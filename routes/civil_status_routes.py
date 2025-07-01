from fastapi import APIRouter

from controllers.civil_status import handle_get_civil_status

civil_status_routes = APIRouter()


@civil_status_routes.get("/civil-status")
def get_civil_status():
    return handle_get_civil_status()
