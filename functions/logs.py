import json
from typing import Optional

from sqlmodel import Session

from database.sqlite import engine
from models.system_log import SystemLog


def log_action(
    action: str,
    table_name: str,
    record_id: Optional[int] = None,
    user_id: Optional[int] = None,
    details: Optional[dict] = None,
    endpoint: Optional[str] = None,
):
    with Session(engine) as session:
        log = SystemLog(
            action=action,
            table_name=table_name,
            record_id=record_id,
            user_id=user_id,
            details=json.dumps(details) if details else None,
            endpoint=endpoint,
        )

        session.add(log)

        session.commit()
