from fastapi import APIRouter

from controllers.discount_reasons import handle_get_discounts_reasons

discount_reasons_routes = APIRouter()


@discount_reasons_routes.get("/discounts-reasons")
def get_discounts_reasons():
    return handle_get_discounts_reasons()
