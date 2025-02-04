from pydantic import BaseModel


class StatusResignableReasonsInput(BaseModel):
    first_day: str
    last_day: str
    resignable_reasons_ids: str
