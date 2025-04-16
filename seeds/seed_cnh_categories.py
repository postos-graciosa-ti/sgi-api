from sqlmodel import Session, select

from database.sqlite import engine
from models.cnh_categories import CnhCategories


def seed_cnh_categories():
    with Session(engine) as session:
        exist_cnh_categories = session.exec(select(CnhCategories)).first()

        if not exist_cnh_categories:
            cnh_categories = [
                CnhCategories(name="A"),
                CnhCategories(name="B"),
                CnhCategories(name="AB"),
            ]

            session.add_all(cnh_categories)

            session.commit()
