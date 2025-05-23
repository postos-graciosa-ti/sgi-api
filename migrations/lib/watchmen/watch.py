import os

from sqlalchemy import inspect, text
from sqlmodel import Session, SQLModel, create_engine

from database.sqlite import engine  # ou postgres, dependendo do seu projeto


def get_column_type(column, dialect):
    """Retorna o tipo SQL apropriado baseado no dialeto."""
    if dialect == "postgresql":
        if "VARCHAR" in str(column.type).upper():
            return "VARCHAR"
        if "TEXT" in str(column.type).upper():
            return "TEXT"
        if "BOOLEAN" in str(column.type).upper():
            return "BOOLEAN"
        if "INTEGER" in str(column.type).upper():
            return "INTEGER"
        if "DATETIME" in str(column.type).upper():
            return "TIMESTAMP"
        if "FLOAT" in str(column.type).upper():
            return "FLOAT"
    # fallback ou sqlite
    return str(column.type).upper()


def watch(model: type[SQLModel]):
    db_dialect = os.environ.get("DIALECTICS", "sqlite").lower()
    inspector = inspect(engine)
    table_name = model.__tablename__
    table_exists = inspector.has_table(table_name)

    existing_columns = set()
    if table_exists:
        existing_columns = {col["name"] for col in inspector.get_columns(table_name)}

    if not table_exists:
        columns = []

        for column in model.__table__.columns:
            col_type = get_column_type(column, db_dialect)
            col_def = f"{column.name} {col_type}"

            if column.primary_key:
                if db_dialect == "postgresql":
                    col_def = f"{column.name} SERIAL PRIMARY KEY"
                else:  # sqlite
                    col_def += " PRIMARY KEY"
                    if column.autoincrement and col_type.startswith("INTEGER"):
                        col_def += " AUTOINCREMENT"

            columns.append(col_def)

        columns_sql = ",\n    ".join(columns)

        query = text(
            f"""
            CREATE TABLE {table_name} (
                {columns_sql}
            )
            """
        )

        with engine.connect() as conn:
            conn.execute(query)
            conn.commit()
    else:
        for column in model.__table__.columns:
            if column.name not in existing_columns:
                col_type = get_column_type(column, db_dialect)
                query = text(
                    f"""
                    ALTER TABLE {table_name}
                    ADD COLUMN {column.name} {col_type}
                    """
                )

                with engine.connect() as conn:
                    conn.execute(query)
                    conn.commit()
