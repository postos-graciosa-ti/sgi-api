from typing import Optional
from sqlmodel import SQLModel, Field, ForeignKey
from datetime import date

class ScaleSignature(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    is_signed: bool = Field(default=False)
    scale_id: int = Field(foreign_key="scale.id")
    worker_id: int = Field(foreign_key="workers.id")
