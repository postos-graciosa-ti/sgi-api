from sqlmodel import Session, select
from database.sqlite import engine
from models.banks import Banks


def seed_banks():
    banks = [Banks(name="Banco do Brasil")]

    with Session(engine) as session:
        has_banks = session.exec(select(Banks)).first()

        if not has_banks:
            session.add_all(banks)

            session.commit()
