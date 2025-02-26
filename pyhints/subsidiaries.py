from pydantic import BaseModel


class PutSubsidiarie(BaseModel):
    name: str
    adress: str
    phone: str
    email: str
    coordinator: int
