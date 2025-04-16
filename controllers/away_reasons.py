from sqlmodel import Session, select

from database.sqlite import engine
from models.away_reasons import AwayReasons


def handle_get_away_reasons():
    with Session(engine) as session:
        away_reasons = session.exec(select(AwayReasons)).all()

        return away_reasons
