from pydantic import BaseModel


class WeekScale(BaseModel):
    initialDate: str
    finalDate: str


class GetScalesByDate(BaseModel):
    initial_date: str
    end_date: str


class PostScaleInput(BaseModel):
    worker_id: int
    worker_turn_id: int
    worker_function_id: int
    subsidiarie_id: int
    days_off: str
    first_day: str
    last_day: str
    ilegal_dates: str


class ScalesReportInput(BaseModel):
    first_day: str
    last_day: str


class PostSomeWorkersScaleInput(BaseModel):
    worker_ids: str
    # worker_turn_id: int
    # worker_function_id: int
    subsidiarie_id: int
    days_off: str
    first_day: str
    last_day: str
    ilegal_dates: str


class WorkerDeactivateInput(BaseModel):
    is_active: bool
    resignation_date: str
    resignation_reason: int


class ScalesPrintInput(BaseModel):
    start_date: str
    end_date: str
    turn_id: int
