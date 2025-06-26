from datetime import datetime

from models.CustomNotification import CustomNotification
from repositories.delete_record import delete_record
from repositories.get_record_by_column import get_record_by_column
from repositories.post_record import post_record


def handle_get_users_custom_notification(id: int):
    return get_record_by_column(CustomNotification, "user_id", id, "multiple")


def handle_post_custom_notification(custom_notification: CustomNotification):
    if isinstance(custom_notification.date, str):
        custom_notification.date = datetime.strptime(
            custom_notification.date, "%Y-%m-%d"
        ).date()

    return post_record(custom_notification)


def handle_delete_custom_notification(id: int):
    return delete_record(CustomNotification, "id", id)
