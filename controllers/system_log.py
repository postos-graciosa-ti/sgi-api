from sqlalchemy import desc
from sqlmodel import Session, select

from database.sqlite import engine
from models.system_log import SystemLog


def handle_get_system_log():
    with Session(engine) as session:
        system_log = session.exec(
            select(SystemLog).order_by(desc(SystemLog.id))
        ).all()

        return system_log
