from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class SystemLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    action: str  # 'create', 'update', 'delete', etc.
    table_name: str
    record_id: Optional[int]
    user_id: Optional[int]  # se quiser logar o usuário
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    details: Optional[str] = None  # informações extras (JSON string, por ex.)
