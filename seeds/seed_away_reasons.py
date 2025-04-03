from sqlmodel import Session, select

from database.sqlite import engine
from models.away_reasons import AwayReasons


def seed_away_reasons():
    with Session(engine) as session:
        exist_away_reasons = session.exec(select(AwayReasons)).all()

        if not exist_away_reasons:
            away_reasons = [
                AwayReasons(name="Auxílio acidente"),
                AwayReasons(name="Auxílio doença"),
                AwayReasons(name="Licença maternidade"),
                AwayReasons(name="Ativo"),
                AwayReasons(name="Férias"),
            ]

            session.add_all(away_reasons)

            session.commit()
