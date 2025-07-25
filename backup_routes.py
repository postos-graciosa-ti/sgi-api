import os
import shutil
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from decouple import config
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from config.database import reconectar_banco
from functions.verify_api_key import verify_api_key

NOME_ARQUIVO = "database.db"

DATABASE_URL = f"sqlite:///{os.path.join(os.getcwd(), NOME_ARQUIVO)}"

SMTP_SERVER = config("SMTP_SERVER")

SMTP_PORT = config("SMTP_PORT")

EMAIL_ORIGEM = config("EMAIL_REMETENTE")

SENHA_APP = config("SENHA")

EMAIL_DESTINO = config("EMAIL_REMETENTE")

FRONT_URL = config("FRONT_URL")

API_KEY = config("API_KEY")

backup_routes = APIRouter(dependencies=[Depends(verify_api_key)])


def enviar_email(caminho_arquivo: str):
    if not os.path.isfile(caminho_arquivo):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")

    msg = MIMEMultipart()

    msg["From"] = EMAIL_ORIGEM

    msg["To"] = EMAIL_DESTINO

    msg["Subject"] = "Backup do banco SQLite"

    with open(caminho_arquivo, "rb") as f:
        part = MIMEBase("application", "octet-stream")

        part.set_payload(f.read())

    encoders.encode_base64(part)

    part.add_header("Content-Disposition", f'attachment; filename="{NOME_ARQUIVO}"')

    msg.attach(part)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()

        smtp.login(EMAIL_ORIGEM, SENHA_APP)

        smtp.send_message(msg)


@backup_routes.post("/enviar-backup")
async def enviar_backup():
    caminho_db = os.path.join(os.getcwd(), NOME_ARQUIVO)

    if not os.path.isfile(caminho_db):
        raise HTTPException(status_code=404, detail="Arquivo do banco não encontrado.")

    try:
        enviar_email(caminho_db)

        return {"status": "success", "message": "Backup enviado por e-mail."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar e-mail: {e}")


@backup_routes.post("/substituir-db")
async def substituir_db(file: UploadFile = File(...)):
    caminho_db = os.path.join(os.getcwd(), NOME_ARQUIVO)

    try:
        with open(caminho_db, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        reconectar_banco()

        return {
            "status": "success",
            "message": f"Arquivo '{NOME_ARQUIVO}' substituído com sucesso e conexão reiniciada.",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao substituir o banco: {e}")
