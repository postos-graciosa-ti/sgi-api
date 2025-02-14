from sqlmodel import Session, select

from database.sqlite import engine
from models.function_logs import FunctionLogs


def handle_get_functions_logs(id: int):
    with Session(engine) as session:
        query = select(FunctionLogs).where(FunctionLogs.subsidiarie_id == id)

        function_logs = session.exec(query).all()

        return function_logs


def handle_post_functions_logs(id: int, function_log: FunctionLogs):
    with Session(engine) as session:
        function_log.subsidiarie_id = id

        session.add(function_log)

        session.commit()

        session.refresh(function_log)

        return function_log
