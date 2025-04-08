from sqlmodel import Session, select
from database.sqlite import engine
from models.banks import Banks


def handle_get_banks():
    with Session(engine) as session:
        banks = session.exec(select(Banks)).all()

        return banks
