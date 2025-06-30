import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

def add_cors_middleware(app):
    load_dotenv()

    origins = [os.environ.get("FRONT_URL"), "http://localhost:5174"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )