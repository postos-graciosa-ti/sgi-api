from sqlmodel import Session, select

from database.sqlite import engine
from models.nationalities import Nationalities


def handle_get_nationalities():
    with Session(engine) as session:
        nationalities = session.exec(select(Nationalities)).all()

        return nationalities


def handle_post_nationalities(nationalitie: Nationalities):
    with Session(engine) as session:
        session.add(nationalitie)

        session.commit()

        session.refresh(nationalitie)

        return nationalitie


def handle_put_nationalities(id: int, nationalitie: Nationalities):
    with Session(engine) as session:
        db_nationalitie = session.exec(
            select(Nationalities).where(Nationalities.id == id)
        ).first()

        db_nationalitie.name = (
            nationalitie.name if nationalitie.name else db_nationalitie.name
        )

        session.add(db_nationalitie)

        session.commit()

        session.refresh(db_nationalitie)

        return db_nationalitie


def handle_delete_nationalities(id: int):
    with Session(engine) as session:
        db_nationalitie = session.exec(
            select(Nationalities).where(Nationalities.id == id)
        ).first()

        session.delete(db_nationalitie)

        session.commit()

        return {"success": True}
