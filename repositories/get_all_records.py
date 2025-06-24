from sqlmodel import Session, select

from database.sqlite import engine


def get_all_records(model):
    with Session(engine) as session:
        all_records = session.exec(select(model)).all()

        return all_records
