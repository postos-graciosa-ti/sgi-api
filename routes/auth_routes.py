from fastapi import APIRouter

from controllers.users import handle_create_user_password, handle_user_login
from models.user import User
from pyhints.users import CreateUserPasswordInput

auth_routes = APIRouter()


@auth_routes.post("/users/create-password")
def create_user_password(userData: CreateUserPasswordInput):
    return handle_create_user_password(userData)


@auth_routes.post("/users/login")
def user_login(user: User):
    return handle_user_login(user)
