from sqlmodel import Session, select

from database.sqlite import engine
from models.system_log import SystemLog


def handle_get_system_log():
    with Session(engine) as session:
        system_log = session.exec(select(SystemLog)).all()

        return system_log
