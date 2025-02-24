from sqlmodel import Session, select

from database.sqlite import engine
from models.subsidiarie_logs import SubsidiarieLogs


def handle_get_subsidiarie_logs():
    with Session(engine) as session:
        subsidiarie_logs = session.exec(select(SubsidiarieLogs)).all()

        return subsidiarie_logs


def handle_post_subsidiaries_logs(subsidiarie_log: SubsidiarieLogs):
    with Session(engine) as session:
        session.add(subsidiarie_log)

        session.commit()

        session.refresh(subsidiarie_log)

        return subsidiarie_log
