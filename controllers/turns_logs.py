from sqlmodel import Session, select

from database.sqlite import engine
from models.TurnsLogs import TurnsLogs


async def handle_get_turns_logs(id: int):
    with Session(engine) as session:
        turns_logs = session.exec(
            select(TurnsLogs).where(TurnsLogs.subsidiarie_id == id)
        ).all()

        return turns_logs


async def handle_post_turns_logs(id: int, turn_log: TurnsLogs):
    with Session(engine) as session:
        turn_log.subsidiarie_id = id

        session.add(turn_log)

        session.commit()

        session.refresh(turn_log)

        return turn_log
