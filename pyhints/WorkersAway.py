from pydantic import BaseModel


class WorkersAway(BaseModel):
    away_start_date: str
    away_end_date: str
    away_reason_id: int
