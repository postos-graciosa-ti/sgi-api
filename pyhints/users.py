from pydantic import BaseModel


class GetUserRoles(BaseModel):
    id: int
    name: str
    email: str
    role: str
    phone: str


class Test(BaseModel):
    arr: str


class VerifyEmail(BaseModel):
    email: str


class ConfirmPassword(BaseModel):
    email: str
    password: str


class ChangeUserPasswordInput(BaseModel):
    email: str
    currentPassword: str
    newPassword: str


class CreateUserPasswordInput(BaseModel):
    email: str
    password: str
