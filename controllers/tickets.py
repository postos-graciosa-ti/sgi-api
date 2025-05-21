import json
from datetime import date, datetime, timedelta

from fastapi import HTTPException
from sqlmodel import Session, select

from database.sqlite import engine
from models.service import Service
from models.tickets import Tickets
from models.tickets_comments import TicketsComments
from models.user import User


def handle_get_tickets_requesting(id: int):
    with Session(engine) as session:
        requesting_user = session.get(User, id)

        if not requesting_user:
            raise HTTPException(status_code=404, detail="Requesting user not found")

        tickets = session.exec(
            select(Tickets)
            .where(Tickets.requesting_id == id)
            .order_by(Tickets.id.desc())
        ).all()

        if not tickets:
            return []

        all_responsible_ids = set()

        service_ids = set()

        for ticket in tickets:
            try:
                responsible_ids = json.loads(ticket.responsibles_ids)

            except (json.JSONDecodeError, TypeError):
                responsible_ids = []

            all_responsible_ids.update(responsible_ids)

            if ticket.service:
                service_ids.add(ticket.service)

        responsibles_map = {
            user.id: user
            for user in session.exec(
                select(User).where(User.id.in_(all_responsible_ids))
            ).all()
        }

        services_map = {
            service.id: service
            for service in session.exec(
                select(Service).where(Service.id.in_(service_ids))
            ).all()
        }

        tickets_data = []

        for ticket in tickets:
            try:
                responsible_ids = json.loads(ticket.responsibles_ids)

            except (json.JSONDecodeError, TypeError):
                responsible_ids = []

            responsibles = [
                responsible.dict()
                for responsible_id in responsible_ids
                if (responsible := responsibles_map.get(responsible_id))
            ]

            tickets_data.append(
                {
                    "ticket_id": ticket.id,
                    "requesting": requesting_user.dict(),
                    "responsibles": responsibles,
                    "service": services_map.get(ticket.service),
                    "description": ticket.description,
                    "is_open": ticket.is_open,
                    "opened_at": ticket.opened_at,
                    "closed_at": ticket.closed_at,
                }
            )

        return tickets_data


def handle_post_tickets(ticket: Tickets):
    with Session(engine) as session:
        session.add(ticket)

        session.commit()

        session.refresh(ticket)

        return ticket


def handle_close_ticket(ticket_id: int):
    with Session(engine) as session:
        ticket = session.get(Tickets, ticket_id)

        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        ticket.is_open = False

        ticket.closed_at = date.today()

        session.add(ticket)

        session.commit()

        return {
            "message": "Ticket fechado com sucesso",
            "closed_at": ticket.closed_at,
        }


def handle_get_tickets_comments(id: int):
    with Session(engine) as session:
        ticket_comments = (
            session.exec(
                select(TicketsComments, User)
                .join(User, TicketsComments.comentator_id == User.id)
                .where(TicketsComments.ticket_id == id)
                .order_by(TicketsComments.ticket_id.asc())
            )
            .mappings()
            .all()
        )

        return ticket_comments


def handle_post_tickets_comments(ticket_comment: TicketsComments):
    with Session(engine) as session:
        session.add(ticket_comment)

        session.commit()

        session.refresh(ticket_comment)

        return ticket_comment


def handle_get_tickets_responsible(id: int):
    with Session(engine) as session:
        responsible_user = session.get(User, id)

        if not responsible_user:
            raise HTTPException(status_code=404, detail="Responsible user not found")

        tickets = session.exec(select(Tickets).order_by(Tickets.id.desc())).all()

        filtered_tickets = []

        for t in tickets:
            try:
                responsible_ids = json.loads(t.responsibles_ids)

            except (json.JSONDecodeError, TypeError):
                responsible_ids = []

            if id in responsible_ids:
                filtered_tickets.append((t, responsible_ids))

        if not filtered_tickets:
            return []

        requesting_ids = {t.requesting_id for t, _ in filtered_tickets}

        all_responsible_ids = set()

        service_ids = set()

        for t, responsible_ids in filtered_tickets:
            all_responsible_ids.update(responsible_ids)

            if t.service:
                service_ids.add(t.service)

        users_map = {
            user.id: user
            for user in session.exec(
                select(User).where(User.id.in_(requesting_ids | all_responsible_ids))
            ).all()
        }

        services_map = {
            service.id: service
            for service in session.exec(
                select(Service).where(Service.id.in_(service_ids))
            ).all()
        }

        tickets_data = []

        for t, responsible_ids in filtered_tickets:
            responsibles = [
                responsible.dict()
                for responsible_id in responsible_ids
                if (responsible := users_map.get(responsible_id))
            ]

            tickets_data.append(
                {
                    "ticket_id": t.id,
                    "requesting": users_map.get(t.requesting_id),
                    "responsibles": responsibles,
                    "service": services_map.get(t.service),
                    "description": t.description,
                    "is_open": t.is_open,
                    "opened_at": t.opened_at,
                    "closed_at": t.closed_at,
                }
            )

        return tickets_data


def handle_get_tickets_responsible(id: int):
    with Session(engine) as session:
        responsible_user = session.get(User, id)

        if not responsible_user:
            raise HTTPException(status_code=404, detail="Responsible user not found")

        tickets = session.exec(select(Tickets).order_by(Tickets.id.desc())).all()

        filtered_tickets = []

        for t in tickets:
            try:
                responsible_ids = json.loads(t.responsibles_ids)

            except (json.JSONDecodeError, TypeError):
                responsible_ids = []

            if id in responsible_ids:
                filtered_tickets.append((t, responsible_ids))

        if not filtered_tickets:
            return []

        requesting_ids = {t.requesting_id for t, _ in filtered_tickets}

        all_responsible_ids = set()

        service_ids = set()

        for t, responsible_ids in filtered_tickets:
            all_responsible_ids.update(responsible_ids)

            if t.service:
                service_ids.add(t.service)

        users_map = {
            user.id: user
            for user in session.exec(
                select(User).where(User.id.in_(requesting_ids | all_responsible_ids))
            ).all()
        }

        services_map = {
            service.id: service
            for service in session.exec(
                select(Service).where(Service.id.in_(service_ids))
            ).all()
        }

        tickets_data = []

        for t, responsible_ids in filtered_tickets:
            responsibles = [
                responsible.dict()
                for responsible_id in responsible_ids
                if (responsible := users_map.get(responsible_id))
            ]

            tickets_data.append(
                {
                    "ticket_id": t.id,
                    "requesting": users_map.get(t.requesting_id),
                    "responsibles": responsibles,
                    "service": services_map.get(t.service),
                    "description": t.description,
                    "is_open": t.is_open,
                    "opened_at": t.opened_at,
                    "closed_at": t.closed_at,
                }
            )

        return tickets_data


def handle_get_tickets_responsible_notifications(id: int):
    with Session(engine) as session:
        today = date.today()

        start_of_week = (today - timedelta(days=today.weekday())).isoformat()

        end_of_week = (
            datetime.fromisoformat(start_of_week) + timedelta(days=6)
        ).isoformat()

        tickets = (
            session.exec(
                select(Tickets, User, Service)
                .join(User, Tickets.requesting_id == User.id)
                .join(Service, Tickets.service == Service.id)
                .where(Tickets.opened_at >= start_of_week)
                .where(Tickets.opened_at <= end_of_week)
                .where(Tickets.responsibles_ids.contains(id))
                .order_by(Tickets.id.desc())
            )
            .mappings()
            .all()
        )

        return tickets
