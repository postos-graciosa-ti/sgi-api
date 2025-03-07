from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlmodel import Session, select

from database.sqlite import engine
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


def handle_post_subsidiaries(formData: Subsidiarie):
    with Session(engine) as session:
        session.add(formData)

        session.commit()

        session.refresh(formData)
    return formData


def handle_put_subsidiarie(id: int, subsidiarie: Subsidiarie):
    with Session(engine) as session:
        db_subsidiarie = session.exec(
            select(Subsidiarie).where(Subsidiarie.id == id)
        ).first()

        if subsidiarie.name:
            db_subsidiarie.name = subsidiarie.name

        if subsidiarie.adress:
            db_subsidiarie.adress = subsidiarie.adress

        if subsidiarie.phone:
            db_subsidiarie.phone = subsidiarie.phone

        if subsidiarie.email:
            db_subsidiarie.email = subsidiarie.email

        if subsidiarie.coordinator is not None:
            db_subsidiarie.coordinator = subsidiarie.coordinator

        if subsidiarie.manager is not None:
            db_subsidiarie.manager = subsidiarie.manager

        session.add(db_subsidiarie)

        session.commit()

        session.refresh(db_subsidiarie)

        return db_subsidiarie


def handle_delete_subsidiarie(id: int):
    with Session(engine) as session:
        subsidiarie = session.get(Subsidiarie, id)

        if subsidiarie:
            session.delete(subsidiarie)

            session.commit()
        return {"message": "Subsidiarie deleted successfully"}
