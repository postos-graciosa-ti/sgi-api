import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException
from jose import jwt

load_dotenv()

secret = os.environ.get("SECRET")

algorithm = os.environ.get("ALGORITHM")


def verify_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid token")

    token = authorization[7:]

    try:
        payload = jwt.decode(token, secret, algorithms=[algorithm])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload
