from pydantic import BaseModel
from sqlmodel import Session

from database.sqlite import engine


class CreateTablesBody(BaseModel):
    model: dict


def handle_create_tables(body: CreateTablesBody):
    with Session(engine) as session:
        query = f"""
            CREATE TABLE IF NOT EXISTS {body.__tablename__} (
            id AUTO INCREMENT PRIMARY KEY,
            name VARCHAR(250)
            )
            """

        session.exec(query)

        session.commit()
