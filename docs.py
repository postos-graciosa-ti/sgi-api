from typing import Optional

from fastapi import FastAPI, File, HTTPException, Response, UploadFile
from sqlmodel import Field, SQLModel


class PDFRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    content: bytes  # Armazenará o binário do PDF
    size: int  # Tamanho do arquivo em bytes


@app.get("/list-pdfs/")
async def list_pdfs():
    with Session(engine) as session:
        pdfs = session.query(PDFRecord).all()

        return [
            {"id": pdf.id, "filename": pdf.filename, "size": pdf.size} for pdf in pdfs
        ]


# @app.get("/view-pdf/{pdf_id}")
# async def view_pdf(pdf_id: int, download: bool = False):
#     with Session(engine) as session:
#         pdf_record = session.get(PDFRecord, pdf_id)
#         if not pdf_record:
#             raise HTTPException(status_code=404, detail="PDF não encontrado")

#         # Define o tipo de resposta com o cabeçalho Content-Disposition
#         disposition = "attachment" if download else "inline"
#         headers = {
#             "Content-Disposition": f'{disposition}; filename="{pdf_record.filename}"'
#         }

#         return Response(
#             content=pdf_record.content, media_type="application/pdf", headers=headers
#         )


@app.get("/view-pdf/{pdf_id}")
async def view_pdf(pdf_id: int):
    with Session(engine) as session:
        pdf_record = session.get(PDFRecord, pdf_id)
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


@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    # Verifica se o arquivo é um PDF
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400, detail="Apenas arquivos PDF são permitidos"
        )

    # Lê o conteúdo do arquivo
    contents = await file.read()
    file_size = len(contents)

    # Cria o registro no banco de dados
    pdf_record = PDFRecord(filename=file.filename, content=contents, size=file_size)

    with Session(engine) as session:
        session.add(pdf_record)
        session.commit()
        session.refresh(pdf_record)

    return {
        "message": "PDF salvo com sucesso",
        "id": pdf_record.id,
        "filename": pdf_record.filename,
        "size": pdf_record.size,
    }