from sqlmodel import Session, select
from database.sqlite import engine
from models.school_levels import SchoolLevels


def seed_school_levels():
    school_levels = [
        SchoolLevels(name="Curso extracurricular"),
        SchoolLevels(name="Fundamental incompleto"),
        SchoolLevels(name="Fundamental completo"),
        SchoolLevels(name="Ensino médio completo"),
        SchoolLevels(name="Curso técnico"),
        SchoolLevels(name="Superior incompleto"),
        SchoolLevels(name="Superior cursando"),
        SchoolLevels(name="Superior completo"),
        SchoolLevels(name="Pós-graduação cursando"),
        SchoolLevels(name="MBA"),
        SchoolLevels(name="Pós-graduação"),
        SchoolLevels(name="Mestrado"),
        SchoolLevels(name="Doutorado"),
        SchoolLevels(name="Pós-doutorado"),
        SchoolLevels(name="Tecnólogo"),
        SchoolLevels(name="Analfabeto"),
        SchoolLevels(name="Quinto ano incompleto"),
        SchoolLevels(name="Quinto ano completo"),
    ]

    with Session(engine) as session:
        has_school_levels = session.exec(select(SchoolLevels)).first()

        if not has_school_levels:
            session.add_all(school_levels)
            session.commit()