from fastapi import APIRouter

from controllers.school_levels import handle_get_school_levels

school_levels_routes = APIRouter()


@school_levels_routes.get("/school-levels")
def get_school_levels():
    return handle_get_school_levels()
