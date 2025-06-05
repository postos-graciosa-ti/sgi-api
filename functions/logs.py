import json
from typing import Optional

from sqlmodel import Session

from models.system_log import SystemLog


def log_action(
    session: Session,
    action: str,
    table_name: str,
    record_id: Optional[int] = None,
    user_id: Optional[int] = None,
    details: Optional[dict] = None,
):
    log = SystemLog(
        action=action,
        table_name=table_name,
        record_id=record_id,
        user_id=user_id,
        details=json.dumps(details) if details else None,
    )

    session.add(log)

    session.commit()
