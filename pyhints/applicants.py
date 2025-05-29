from pydantic import BaseModel


class RecruitProps(BaseModel):
    applicant_id: int
    worker_data: dict


class SendFeedbackEmailBody(BaseModel):
    id: int
    name: str
    email: str
    message: str
