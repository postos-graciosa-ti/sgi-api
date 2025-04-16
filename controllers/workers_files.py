from fastapi import HTTPException, Response
from sqlmodel import Session, select

from database.sqlite import engine
from models.workers_files import WorkersFiles


def handle_get_workers_files_ids(id: int):
    with Session(engine) as session:
        workers_files_ids = session.exec(
            select(WorkersFiles.id).where(WorkersFiles.worker_id == id)
        ).all()

        return workers_files_ids


async def handle_get_worker_file_by_id(id: int):
    with Session(engine) as session:
        pdf_record = session.get(WorkersFiles, id)

        if not pdf_record:
            raise HTTPException(status_code=404, detail="PDF não encontrado")

        return Response(
            content=pdf_record.content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'inline; filename="{pdf_record.filename}"',
                "Access-Control-Expose-Headers": "Content-Disposition",
            },
        )
