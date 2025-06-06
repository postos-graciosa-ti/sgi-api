from fastapi import APIRouter

from controllers.root import handle_get_docs_info, handle_health_check

root_routes = APIRouter()


@root_routes.get("/")
def get_docs_info():
    return handle_get_docs_info()


@root_routes.get("/health-check")
def health_check():
    return handle_health_check()
