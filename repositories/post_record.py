from sqlmodel import Session

from database.sqlite import engine


def post_record(data):
    with Session(engine) as session:
        session.add(data)

        session.commit()

        session.refresh(data)

        return data
