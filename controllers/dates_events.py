from datetime import date, datetime, timedelta

from sqlmodel import Session, select

from database.sqlite import engine
from models.dates_events import DatesEvents


def handle_get_dates_events(id: int):
    with Session(engine) as session:
        today = date.today()

        first_day = today.replace(day=1)

        if today.month == 12:
            next_month = today.replace(year=today.year + 1, month=1, day=1)

        else:
            next_month = today.replace(month=today.month + 1, day=1)

        last_day = next_month - timedelta(days=1)

        date_events = session.exec(
            select(DatesEvents)
            .where(DatesEvents.subsidiarie_id == id)
            .where(DatesEvents.date.between(first_day, last_day))
        ).all()

        parsed_events = []

        for event in date_events:
            event_dict = event.dict()

            if isinstance(event_dict["date"], str):
                event_dict["date"] = datetime.strptime(
                    event_dict["date"], "%Y-%m-%d"
                ).date()

            parsed_events.append(event_dict)

        return parsed_events


def handle_get_events_by_date(subsidiarie_id: int, date: str):
    with Session(engine) as session:
        dates_events = session.exec(
            select(DatesEvents)
            .where(DatesEvents.subsidiarie_id == subsidiarie_id)
            .where(DatesEvents.date == date)
        ).all()

        return dates_events


def handle_post_dates_events(id: int, date_event: DatesEvents):
    date_event.subsidiarie_id = id

    with Session(engine) as session:
        session.add(date_event)

        session.commit()

        session.refresh(date_event)

        return date_event


def delete_date_event(subsidiarie_id: int, event_id: int):
    with Session(engine) as session:
        date_event = session.exec(
            select(DatesEvents)
            .where(DatesEvents.id == event_id)
            .where(DatesEvents.subsidiarie_id == subsidiarie_id)
        ).first()

        session.delete(date_event)

        session.commit()

        return {"success": True}


def handle_delete_dates_events(subsidiarie_id: int, event_id: int):
    with Session(engine) as session:
        date_event = session.exec(
            select(DatesEvents)
            .where(DatesEvents.id == event_id)
            .where(DatesEvents.subsidiarie_id == subsidiarie_id)
        ).first()

        session.delete(date_event)

        session.commit()

        return {"success": True}
