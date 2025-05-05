from sqlmodel import Session, select

from database.sqlite import engine
from models.service import Service


def seed_services():
    with Session(engine) as session:
        existing_roles = session.exec(select(Service)).all()

        if not existing_roles:
            roles = [Service(name="Advertência"), Service(name="Manutenção do sistema")]

            session.add_all(roles)

            session.commit()
