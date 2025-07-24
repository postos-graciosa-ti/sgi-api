import os
import shutil
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from functions.verify_api_key import verify_api_key

backup_routes = APIRouter(dependencies=[Depends(verify_api_key)])

FILE_NAME = os.environ.get("FILE_NAME", "database.db")


@backup_routes.post("/send-backup")
async def send_backup():
    SMTP_SERVER = os.environ.get("SMTP_SERVER")

    SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))

    EMAIL_SENDER = os.environ.get("EMAIL_REMETENTE")

    APP_PASSWORD = os.environ.get("SENHA")

    EMAIL_RECIPIENT = os.environ.get("EMAIL_REMETENTE")

    EMAIL_CC = os.environ.get("BCC")

    if not all([SMTP_SERVER, EMAIL_SENDER, APP_PASSWORD, EMAIL_RECIPIENT]):
        raise HTTPException(
            status_code=500,
            detail="Missing environment variables required to send email.",
        )

    file_path = os.path.join(os.getcwd(), FILE_NAME)

    if not os.path.isfile(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"File '{FILE_NAME}' not found in the root directory.",
        )

    try:
        msg = MIMEMultipart()

        msg["From"] = EMAIL_SENDER

        msg["To"] = EMAIL_RECIPIENT

        if EMAIL_CC:
            msg["Cc"] = EMAIL_CC

        msg["Subject"] = "SQLite Database Backup"

        with open(file_path, "rb") as file:
            attachment = MIMEBase("application", "octet-stream")

            attachment.set_payload(file.read())

            encoders.encode_base64(attachment)

            attachment.add_header(
                "Content-Disposition",
                f'attachment; filename="{os.path.basename(file_path)}"',
            )

            msg.attach(attachment)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()

            smtp.login(EMAIL_SENDER, APP_PASSWORD)

            smtp.send_message(msg)

        return {"status": "success", "message": "Backup sent via email."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")


@backup_routes.post("/replace-db")
async def replace_db(file: UploadFile = File(...)):
    db_path = os.path.join(os.getcwd(), FILE_NAME)

    try:
        with open(db_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {e}")

    return {
        "status": "success",
        "message": f"File '{FILE_NAME}' successfully replaced.",
    }
