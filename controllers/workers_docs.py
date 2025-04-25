

def handle_delete_workers_docs(id: int):
    with Session(engine) as session:
        doc = session.exec(select(WorkersDocs).where(WorkersDocs.id == id)).first()

        session.delete(doc)

        session.commit()

        return {"success": True}