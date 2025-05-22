import os

from sqlalchemy import text
from sqlmodel import Session

from database.sqlite import engine


def add_coordinator_observations_to_applicants():
    db_dialetics = os.environ.get("DIALETICS")

    with Session(engine) as session:
        if db_dialetics == "sqlite":
            result = session.exec(text("PRAGMA table_info(applicants)"))

            columns = [row[1] for row in result]

            if "coordinator_observations" not in columns:
                session.exec(
                    text(
                        "ALTER TABLE applicants ADD COLUMN coordinator_observations TEXT"
                    )
                )

                session.commit()

        else:
            result = session.exec(
                text(
                    """
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_name = 'applicants' AND column_name = 'coordinator_observations'
                    """
                )
            )

            column_exists = result.first() is not None

            if not column_exists:
                session.exec(
                    text(
                        "ALTER TABLE applicants ADD COLUMN coordinator_observations TEXT"
                    )
                )

                session.commit()
