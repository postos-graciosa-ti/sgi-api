from sqlmodel import Session, select, text
from database.sqlite import engine

def find_all(Model: dict):
  with Session(engine) as session:
    statement = select(Model)
    
    rows = session.exec(statement).all()

  return rows

def create(form_data: dict):
  with Session(engine) as session:
    session.add(form_data)
    
    session.commit()
    
    session.refresh(form_data)
    
    return form_data

# def update(id: int, Model: dict):
#   with Session(engine) as session:
#     statement = select(Model).where(Model.id == id)
    
#     session.exec(statement)
    
#     session.commit()
    
#     session.refresh(Model)
    
#     return Model
