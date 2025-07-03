from fastapi import APIRouter

from controllers.banks import handle_get_banks

banks_routes = APIRouter()


@banks_routes.get("/banks")
def get_banks():
    return handle_get_banks()
