from pydantic import BaseModel


class GetUserRoles(BaseModel):
    id: int
    name: str
    email: str
    role: str


class Test(BaseModel):
    arr: str


class VerifyEmail(BaseModel):
    email: str


class ConfirmPassword(BaseModel):
    email: str
    password: str
