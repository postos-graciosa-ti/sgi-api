from pydantic import BaseModel


class PostWorkerNotationInput(BaseModel):
    notation: str


class WorkerLogCreateInput(BaseModel):
    created_at: str
    created_at_time: str
    user_id: int
    worker_id: int


class WorkerLogUpdateInput(BaseModel):
    updated_at: str
    updated_at_time: str
    user_id: int
    worker_id: int


class WorkerLogDeleteInput(BaseModel):
    deleted_at: str
    deleted_at_time: str
    user_id: int
    worker_id: int
