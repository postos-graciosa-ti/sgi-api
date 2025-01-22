from sqlmodel import Field, Session, SQLModel, create_engine, select

class Workers(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    function_id: int = Field(default=None, foreign_key="function.id")
    subsidiarie_id: int = Field(default=None, foreign_key="subsidiarie.id")
    is_active: bool = Field(default=True)
    turn_id: int = Field(default=None, foreign_key="turn.id")
    cost_center_id: int = Field(default=None, foreign_key="costcenter.id")
    department_id: int = Field(default=None, foreign_key="department.id")
    # security_password: str | None = Field(default=None, nullable=True)
