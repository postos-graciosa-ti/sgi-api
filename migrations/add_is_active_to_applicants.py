import os

from sqlalchemy import text
from sqlmodel import Session

from database.sqlite import engine


def add_is_active_to_applicants():
    db_dialetics = os.environ.get("DIALETICS")

    with Session(engine) as session:
        if db_dialetics == "sqlite":
            result = session.exec(text("PRAGMA table_info(applicants)"))

            columns = [row[1] for row in result]

            if "is_active" not in columns:
                session.exec(
                    text("ALTER TABLE applicants ADD COLUMN is_active BOOLEAN DEFAULT TRUE")
                )

                session.commit()

        else:
            result = session.exec(
                text(
                    """
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_name = 'applicants' AND column_name = 'is_active'
                    """
                )
            )

            column_exists = result.first() is not None

            if not column_exists:
                session.exec(
                    text("ALTER TABLE applicants ADD COLUMN is_active BOOLEAN DEFAULT TRUE")
                )

                session.commit()
