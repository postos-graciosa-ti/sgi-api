from sqlmodel import Field, SQLModel


class RedirectedTo(SQLModel, table=True):
    id: int = Field(primary_key=True)
    applicant_id: int = Field(foreign_key="applicants.id")
    user_id: int = Field(foreign_key="user.id")
    redirected_by: int = Field(foreign_key="user.id")
    subsidiarie_id: int = Field(foreign_key="user.id")
    datetime: str
