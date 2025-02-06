from pydantic import BaseModel


class PostWorkerNotationInput(BaseModel):
    notation: str
