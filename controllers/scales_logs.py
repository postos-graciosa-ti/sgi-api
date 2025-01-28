from sqlmodel import Field, Session, SQLModel, create_engine, select

from database.sqlite import engine
from models.scale_logs import ScaleLogs
from models.user import User
from models.workers import Workers


async def handle_get_scales_logs():
    with Session(engine) as session:
        scales_logs = session.exec(
            select(ScaleLogs.inserted_at, ScaleLogs.at_time, Workers.name, User.name)
            .join(Workers, ScaleLogs.worker_id == Workers.id)
            .join(User, ScaleLogs.user_id == User.id)
            .order_by(ScaleLogs.id.desc())
        ).all()

        return [
            {
                "inserted_at": scale_log[0],
                "at_time": scale_log[1],
                "worker_name": scale_log[2],
                "user_name": scale_log[3],
            }
            for scale_log in scales_logs
        ]


async def handle_post_scale_logs(scales_logs_input: ScaleLogs):
    with Session(engine) as session:
        session.add(scales_logs_input)

        session.commit()

        session.refresh(scales_logs_input)
    return scales_logs_input
