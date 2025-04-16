from sqlmodel import Session, select

from database.sqlite import engine
from models.cnh_categories import CnhCategories


def handle_get_cnh_categories():
    with Session(engine) as session:
        cnh_categories = session.exec(select(CnhCategories)).all()

        return cnh_categories
