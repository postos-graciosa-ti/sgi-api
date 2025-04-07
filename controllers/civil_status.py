from sqlmodel import Session, select

from database.sqlite import engine
from models.civil_status import CivilStatus


def handle_get_civil_status():
    with Session(engine) as session:
        civil_status = session.exec(select(CivilStatus)).all()

        return civil_status
