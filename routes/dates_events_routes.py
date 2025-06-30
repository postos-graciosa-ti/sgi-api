from fastapi import APIRouter, Depends

from controllers.dates_events import (
    handle_delete_dates_events,
    handle_get_dates_events,
    handle_get_events_by_date,
    handle_post_dates_events,
)
from functions.auth import verify_token
from models.dates_events import DatesEvents

dates_events_routes = APIRouter()


@dates_events_routes.get(
    "/subsidiaries/{subsidiarie_id}/dates-events", dependencies=[Depends(verify_token)]
)
def get_dates_events(subsidiarie_id: int):
    return handle_get_dates_events(subsidiarie_id)


@dates_events_routes.get(
    "/subsidiaries/{subsidiarie_id}/dates/{date}/dates-events",
    dependencies=[Depends(verify_token)],
)
def get_events_by_date(subsidiarie_id: int, date: str):
    return handle_get_events_by_date(subsidiarie_id, date)


@dates_events_routes.post(
    "/subsidiaries/{id}/dates-events", dependencies=[Depends(verify_token)]
)
def post_date_event(id: int, date_event: DatesEvents):
    return handle_post_dates_events(id, date_event)


@dates_events_routes.delete(
    "/subsidiaries/{subsidiarie_id}/dates-events/{event_id}",
    dependencies=[Depends(verify_token)],
)
def delete_date_event(subsidiarie_id: int, event_id: int):
    return handle_delete_dates_events(subsidiarie_id, event_id)
