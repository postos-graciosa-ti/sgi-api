from sqlmodel import Session, select

from database.sqlite import engine
from models.hierarchy_structure import HierarchyStructure


def seed_hierarchy_structure():
    with Session(engine) as session:
        exists_structure = session.exec(select(HierarchyStructure)).first()

        if not exists_structure:
            structures = [
                HierarchyStructure(name="Operacional"),
                HierarchyStructure(name="Tático"),
                HierarchyStructure(name="Estratégico"),
            ]

            session.add_all(structures)

            session.commit()
