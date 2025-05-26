from sqlmodel import Field, SQLModel


class OpenPositions(SQLModel, table=True):
    __tablename__ = "openpositions"

    id: int | None = Field(default=None, primary_key=True)
    subsidiarie_id: int = Field(default=None, foreign_key="subsidiarie.id", index=True)
    function_id: int = Field(default=None, foreign_key="function.id", index=True)
    turn_id: int = Field(default=None, foreign_key="turn.id", index=True)
