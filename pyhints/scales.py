from pydantic import BaseModel

class WeekScale(BaseModel):
  initialDate: str
  finalDate: str

class GetScalesByDate(BaseModel):
    initial_date: str
    end_date: str
