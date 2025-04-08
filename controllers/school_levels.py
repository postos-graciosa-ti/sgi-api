from sqlmodel import Session, select

from database.sqlite import engine
from models.school_levels import SchoolLevels


def handle_get_school_levels():
    with Session(engine) as session:
        school_levels = session.exec(select(SchoolLevels)).all()

        return school_levels
