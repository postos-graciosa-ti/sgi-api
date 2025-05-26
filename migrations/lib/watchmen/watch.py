import os

from sqlalchemy import inspect, text
from sqlmodel import Session, SQLModel, create_engine

from database.sqlite import engine


def get_column_type(column, dialect):
    col_type_str = str(column.type).upper()

    if dialect == "postgresql":
        if "VARCHAR" in col_type_str:
            return "VARCHAR"

        if "TEXT" in col_type_str:
            return "TEXT"

        if "BOOLEAN" in col_type_str:
            return "BOOLEAN"

        if "INTEGER" in col_type_str:
            return "INTEGER"

        if "DATETIME" in col_type_str:
            return "TIMESTAMP"

        if "FLOAT" in col_type_str:
            return "FLOAT"

    return col_type_str


def watch(model: type[SQLModel], use_identity: bool = False):
    db_dialect = os.environ.get("DIALETICS", "postgresql").lower()

    assert db_dialect in (
        "sqlite",
        "postgresql",
    ), f"Dialeto não suportado: {db_dialect}"

    print(f"Usando o dialeto: {db_dialect}")

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
                    if use_identity:
                        col_def = f"{column.name} INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY"

                    else:
                        col_def = f"{column.name} SERIAL PRIMARY KEY"

                elif db_dialect == "sqlite":
                    if column.autoincrement and col_type.startswith("INTEGER"):
                        col_def = f"{column.name} INTEGER PRIMARY KEY AUTOINCREMENT"

                    else:
                        col_def += " PRIMARY KEY"

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
