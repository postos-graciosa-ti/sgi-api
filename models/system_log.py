from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class SystemLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    action: str
    table_name: str
    record_id: Optional[int]
    user_id: Optional[int]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    details: Optional[str] = None
    endpoint: str
