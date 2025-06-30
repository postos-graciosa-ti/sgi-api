from models.workers_metrics import WorkersMetrics
from repositories.get_record_by_column import get_record_by_column
from repositories.post_record import post_record


def handle_get_workers_metrics_by_id(id):
    return get_record_by_column(WorkersMetrics, "worker_id", id, "multiple")


def handle_post_workers_metrics(workers_metrics):
    return post_record(workers_metrics)
