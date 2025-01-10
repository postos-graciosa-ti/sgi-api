from fastapi.responses import JSONResponse
from sqlmodel import Session, select

from database.sqlite import engine
from models.candidate import Candidate
from models.jobs import Jobs


def handle_get_candidates():
    with Session(engine) as session:
        candidates = session.exec(select(Candidate)).all()
    return candidates


def handle_get_candidates_by_status(id: int):
    with Session(engine) as session:
        statement = (
            select(
                Candidate.id,
                Candidate.name,
                Candidate.date_of_birth,
                Candidate.adress,
                Candidate.resume,
                Candidate.status,
                Jobs.id.label("job_id"),
                Jobs.name.label("job_name"),
            )
            .join(Jobs, Candidate.job_id == Jobs.id)
            .where(Candidate.status == id)
        )

        candidates = session.exec(statement).all()

        return JSONResponse(
            [
                {
                    "candidate_id": candidate[0],
                    "name": candidate[1],
                    "date_of_birth": candidate[2],
                    "adress": candidate[3],
                    "resume": candidate[4],
                    "status": candidate[5],
                    "job_id": candidate[6],
                    "job_name": candidate[7],
                }
                for candidate in candidates
            ]
        )


def handle_post_candidate(candidate: Candidate):
    with Session(engine) as session:
        new_candidate = Candidate(
            name=candidate.name,
            date_of_birth=candidate.date_of_birth,
            adress="candidate.adress",
            resume=candidate.resume,
            job_id=candidate.job_id,
            status=2,
        )

        session.add(new_candidate)

        session.commit()

        session.refresh(new_candidate)

    return new_candidate
