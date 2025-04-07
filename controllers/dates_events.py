from datetime import date, datetime, timedelta

from sqlmodel import Session, select

from database.sqlite import engine
from models.dates_events import DatesEvents


def handle_get_date_event(id: int):
    with Session(engine) as session:
        today = date.today()

        first_day = today.replace(day=1)

        last_day = today.replace(day=1).replace(month=today.month + 1) - timedelta(
            days=1
        )

        date_event = session.exec(
            select(DatesEvents)
            .where(DatesEvents.subsidiarie_id == id)
            .where(DatesEvents.date.between(first_day, last_day))
        ).all()

        return date_event


def handle_get_events_by_date(id: int, date: str):
    with Session(engine) as session:
        dates_events = session.exec(
            select(DatesEvents)
            .where(DatesEvents.subsidiarie_id == id)
            .where(DatesEvents.date == date)
        ).all()

        return dates_events


def handle_post_date_event(id: int, date_event: DatesEvents):
    date_event.subsidiarie_id = id

    with Session(engine) as session:
        session.add(date_event)

        session.commit()

        session.refresh(date_event)

        return date_event


def handle_delete_date_event(subsidiarie_id: int, event_id: int):
    with Session(engine) as session:
        date_event = session.exec(
            select(DatesEvents)
            .where(DatesEvents.id == event_id)
            .where(DatesEvents.subsidiarie_id == subsidiarie_id)
        ).first()

        session.delete(date_event)

        session.commit()

        return {"success": True}
