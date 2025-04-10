from sqlmodel import Session, select

from database.sqlite import engine
from models.hierarchy_structure import HierarchyStructure


def handle_get_hierarchy_structure():
    with Session(engine) as session:
        hierarchy_structure = session.exec(select(HierarchyStructure)).all()

        return hierarchy_structure
