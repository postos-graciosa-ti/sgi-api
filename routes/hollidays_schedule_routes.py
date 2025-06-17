from fastapi import APIRouter

from controllers.hollidays_scale import (
    handle_get_holliday_schedule,
    handle_post_holliday_schedule,
)
from models.hollidays_scale import HollidaysScale

hollidays_schedule_routes = APIRouter()


@hollidays_schedule_routes.get("/subsidiaries/{id}/holliday-schedule/{date}")
def get_holliday_schedule(id: int, date: str):
    return handle_get_holliday_schedule(id, date)


@hollidays_schedule_routes.post("/holliday-schedule")
def post_holliday_schedule(holliday_schedule: HollidaysScale):
    return handle_post_holliday_schedule(holliday_schedule)
