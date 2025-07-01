from fastapi import APIRouter

from controllers.workers_discounts import (
    handle_get_workers_discounts,
    handle_post_workers_discounts,
)
from models.workers_discounts import WorkersDiscounts

workers_discounts_routes = APIRouter()


@workers_discounts_routes.get("/workers-discounts/{worker_id}")
def get_workers_discounts(worker_id):
    return handle_get_workers_discounts(worker_id)


@workers_discounts_routes.post("/workers-discounts")
def post_workers_discounts(worker_discount: WorkersDiscounts):
    return handle_post_workers_discounts(worker_discount)
