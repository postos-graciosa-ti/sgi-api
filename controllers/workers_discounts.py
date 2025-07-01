from models.workers_discounts import WorkersDiscounts
from repositories.get_record_by_column import get_record_by_column
from repositories.post_record import post_record


def handle_get_workers_discounts(worker_id):
    return get_record_by_column(WorkersDiscounts, "worker_id", worker_id, "multiple")


def handle_post_workers_discounts(worker_discount):
    return post_record(worker_discount)
