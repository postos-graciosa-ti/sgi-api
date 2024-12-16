from sqlmodel import Field, Session, SQLModel, create_engine, select
from dotenv import load_dotenv
import os

load_dotenv()

sqlite_url = os.environ.get("SQLITE_URL")

connect_args = {"check_same_thread": False}

engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)