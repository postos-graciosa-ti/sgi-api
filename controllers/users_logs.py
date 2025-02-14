from sqlmodel import Session, select

from database.sqlite import engine
from models.users_logs import UsersLogs


def handle_get_logs_user():
    with Session(engine) as session:
        users_logs = session.exec(select(UsersLogs)).all()

        return users_logs


def handle_post_logs_user(users_logs: UsersLogs):
    with Session(engine) as session:
        session.add(users_logs)

        session.commit()

        session.refresh(users_logs)

        return users_logs
