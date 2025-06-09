from fastapi import Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlmodel import Session, select

from database.sqlite import engine
from functions.auth import AuthUser
from functions.logs import log_action
from models.subsidiarie import Subsidiarie
from pyhints.subsidiaries import PutSubsidiarie


def handle_get_subsidiaries():
    with Session(engine) as session:
        subsidiaries = session.exec(select(Subsidiarie)).all()

        return subsidiaries


def handle_get_subsidiarie_by_id(id: int):
    with Session(engine) as session:
        subsidiarie = session.exec(
            select(Subsidiarie).where(Subsidiarie.id == id)
        ).one()

        return subsidiarie


def handle_post_subsidiaries(request: Request, formData: Subsidiarie, user: AuthUser):
    with Session(engine) as session:
        session.add(formData)

        session.commit()

        session.refresh(formData)

        log_action(
            action="post",
            table_name="subsidiaries",
            record_id=formData.id,
            user_id=user["id"],
            details={
                "before": None,
                "after": formData.dict(),
            },
            endpoint=str(request.url.path),
        )

        return formData


def handle_put_subsidiarie(
    id: int, formData: Subsidiarie, request: Request, user: AuthUser
):
    with Session(engine) as session:
        db_subsidiarie = session.exec(
            select(Subsidiarie).where(Subsidiarie.id == id)
        ).first()

        old_values = db_subsidiarie.dict()

        for field, value in formData.dict(exclude_unset=True).items():
            current_value = getattr(db_subsidiarie, field)

            if current_value != value:
                setattr(db_subsidiarie, field, value)

        session.add(db_subsidiarie)

        session.commit()

        session.refresh(db_subsidiarie)

        if db_subsidiarie.dict() != old_values:
            log_action(
                action="put",
                table_name="subsidiaries",
                record_id=id,
                user_id=user["id"],
                details={
                    "before": old_values,
                    "after": db_subsidiarie.dict(),
                },
                endpoint=str(request.url.path),
            )

        return db_subsidiarie


def handle_delete_subsidiarie(request: Request, id: int, user: AuthUser):
    with Session(engine) as session:
        subsidiarie = session.get(Subsidiarie, id)

        old_data = subsidiarie.dict()

        session.delete(subsidiarie)

        session.commit()

        log_action(
            action="delete",
            table_name="subsidiaries",
            record_id=id,
            user_id=user["id"],
            details={
                "before": old_data,
                "after": None,
            },
            endpoint=str(request.url.path),
        )

        return {"message": "Subsidiária deletada com sucesso"}
