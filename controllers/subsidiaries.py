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


def handle_put_subsidiarie(id: int, formData: PutSubsidiarie):
    with Session(engine) as session:
        subsidiarie = session.get(Subsidiarie, id)

        if formData.name:
            subsidiarie.name = formData.name

        if formData.adress:
            subsidiarie.adress = formData.adress

        if formData.phone:
            subsidiarie.phone = formData.phone

        if formData.email:
            subsidiarie.email = formData.email

        if formData.coordinator:
            subsidiarie.coordinator = formData.coordinator

        session.commit()

        session.refresh(subsidiarie)

        return subsidiarie


def handle_delete_subsidiarie(id: int):
    with Session(engine) as session:
        subsidiarie = session.get(Subsidiarie, id)

        if subsidiarie:
            session.delete(subsidiarie)

            session.commit()
        return {"message": "Subsidiarie deleted successfully"}
