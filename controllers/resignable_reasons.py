from sqlmodel import Session, select

from database.sqlite import engine
from models.resignable_reasons import ResignableReasons


async def handle_get_resignable_reasons():
    with Session(engine) as session:
        resignable_reasons = session.exec(select(ResignableReasons)).all()

    return resignable_reasons
