from sqlmodel import Field, Session, SQLModel, create_engine, select


class Applicants(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(default=None, nullable=True)
    desired_function: int = Field(default=None, foreign_key="function.id", index=True)
    nature: str = Field(default=None, nullable=True)
    how_long: str = Field(default=None, nullable=True)
    experience_function: str = Field(default=None, nullable=True)
    redirect_to: int = Field(
        default=None, nullable=True, foreign_key="user.id", index=True
    )
    coordinator_observation: str = Field(default=None, nullable=True)
