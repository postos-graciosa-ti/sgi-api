from pydantic import BaseModel


class WeekScale(BaseModel):
    initialDate: str
    finalDate: str


class GetScalesByDate(BaseModel):
    initial_date: str
    end_date: str


class PostScaleInput(BaseModel):
    worker_id: int
    subsidiarie_id: int
    days_off: str
    first_day: str
    last_day: str
