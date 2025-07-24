import os

from decouple import config
from fastapi import Header, HTTPException


def verify_api_key(x_api_key: str = Header(...)):
    API_KEY = config("API_KEY")

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
