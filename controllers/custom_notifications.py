import os
import smtplib
from datetime import date, datetime
from email.message import EmailMessage

from sqlmodel import Session, select

from database.sqlite import engine
from models.CustomNotification import CustomNotification
from models.user import User
from repositories.delete_record import delete_record
from repositories.get_record_by_column import get_record_by_column
from repositories.post_record import post_record


def handle_get_users_custom_notification(id: int):
    return get_record_by_column(CustomNotification, "user_id", id, "multiple")


def handle_verify_custom_notifications():
    today = date.today()

    EMAIL_REMETENTE = os.environ.get("EMAIL_REMETENTE")

    SENHA = os.environ.get("SENHA")

    BCC = os.environ.get("BCC")

    with Session(engine) as session:
        notifications = session.exec(
            select(CustomNotification).where(CustomNotification.date == today)
        ).all()

        if not notifications:
            return {"message": "No notifications for today."}

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_REMETENTE, SENHA)

            for notification in notifications:
                user = session.get(User, notification.user_id)

                if not user or not user.email:
                    continue

                msg = EmailMessage()

                msg["Subject"] = notification.title

                msg["From"] = EMAIL_REMETENTE

                msg["To"] = user.email

                if BCC:
                    msg["Bcc"] = BCC

                msg.set_content(notification.description)

                smtp.send_message(msg)

    return {"message": f"{len(notifications)} notification(s) sent successfully."}


def handle_post_custom_notification(custom_notification: CustomNotification):
    if isinstance(custom_notification.date, str):
        custom_notification.date = datetime.strptime(
            custom_notification.date, "%Y-%m-%d"
        ).date()

    return post_record(custom_notification)


def handle_delete_custom_notification(id: int):
    return delete_record(CustomNotification, "id", id)
