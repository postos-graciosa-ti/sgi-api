from fastapi import APIRouter

from controllers.custom_notifications import (
    handle_delete_custom_notification,
    handle_get_users_custom_notification,
    handle_post_custom_notification,
)
from models.CustomNotification import CustomNotification

custom_notifications_routes = APIRouter()


@custom_notifications_routes.get("/users/{id}/custom-notifications")
def get_users_custom_notification(id: int):
    return handle_get_users_custom_notification(id)


@custom_notifications_routes.post("/custom-notification")
def post_custom_notification(custom_notification: CustomNotification):
    return handle_post_custom_notification(custom_notification)


@custom_notifications_routes.delete("/custom-notification/{id}")
def delete_custom_notification(id: int):
    return handle_delete_custom_notification(id)
