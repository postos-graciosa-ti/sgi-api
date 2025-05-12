from pydantic import BaseModel


class RecruitProps(BaseModel):
    applicant_id: int
    worker_data: dict
