from io import BytesIO
from typing import List, Optional

import PyPDF2
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from sqlmodel import Column, Field, LargeBinary, Session, SQLModel, select


class WorkersDocs(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    worker_id: int = Field(foreign_key="workers.id")
    doc: bytes = Field(sa_column=Column(LargeBinary))
    doc_title: str = Field(max_length=100)
