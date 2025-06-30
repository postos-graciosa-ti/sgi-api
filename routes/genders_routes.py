from fastapi import APIRouter

from controllers.genders import handle_get_genders

genders_routes = APIRouter()


@genders_routes.get("/genders")
def get_genders():
    return handle_get_genders()
