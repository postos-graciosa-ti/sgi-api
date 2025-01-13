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
        subsidiarie = session.exec(
            select(Subsidiarie).where(Subsidiarie.id == id)
        ).first()

        if subsidiarie:
            subsidiarie.name = formData.name

            subsidiarie.adress = formData.adress

            subsidiarie.phone = formData.phone

            subsidiarie.email = formData.email

            session.add(subsidiarie)

            session.commit()

            session.refresh(subsidiarie)

            return subsidiarie
        return JSONResponse(
            status_code=404, content={"message": "Subsidiarie not found"}
        )


def handle_delete_subsidiarie(id: int):
    with Session(engine) as session:
        subsidiarie = session.get(Subsidiarie, id)

        if subsidiarie:
            session.delete(subsidiarie)

            session.commit()
        return {"message": "Subsidiarie deleted successfully"}
