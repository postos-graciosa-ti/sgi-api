from sqlmodel import Session, select

from database.sqlite import engine
from models.service import Service


def handle_get_services():
    with Session(engine) as session:
        services = session.exec(select(Service)).all()

        return services
