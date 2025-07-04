from fastapi import APIRouter, Depends, File, UploadFile

from controllers.applicants import (
    handle_delete_applicants,
    handle_get_applicant_docs_by_applicant_id,
    handle_get_applicant_process,
    handle_get_applicants,
    handle_get_applicants_approved,
    handle_get_applicants_exams,
    handle_get_applicants_in_process,
    handle_get_applicants_notifications,
    handle_get_applicants_redirected_to,
    handle_get_applicants_reproved,
    handle_get_document_file_by_id,
    handle_patch_applicants,
    handle_post_applicant,
    handle_post_applicants_docs,
    handle_post_applicants_exams,
    handle_post_applicants_redirected_to,
    handle_post_hire_applicants,
    handle_post_send_feedback_email,
    handle_upsert_applicant_process,
)
from functions.auth import verify_token
from models.applicant_process import ApplicantProcess
from models.applicants import Applicants
from models.applicants_exams import ApplicantsExams
from models.redirected_to import RedirectedTo
from pyhints.applicants import RecruitProps, SendFeedbackEmailBody

routes = APIRouter()


@routes.get("/applicants")
def get_applicants():
    return handle_get_applicants()


@routes.get("/applicants/in-process")
def get_applicants_in_process():
    return handle_get_applicants_in_process()


@routes.get("/applicants/approved")
def get_applicants_approved():
    return handle_get_applicants_approved()


@routes.get("/applicants/reproved")
def get_applicants_reproved():
    return handle_get_applicants_reproved()


@routes.post("/applicants")
def post_applicant(applicant: Applicants):
    return handle_post_applicant(applicant)


@routes.patch("/applicants/{id}")
def patch_applicants(id: int, applicant: Applicants):
    return handle_patch_applicants(id, applicant)


@routes.delete("/applicants/{id}")
def delete_applicants(id: int):
    return handle_delete_applicants(id)


@routes.post("/applicants/hire")
def post_hire_applicants(recruit: RecruitProps):
    return handle_post_hire_applicants(recruit)


@routes.get("/users/{id}/applicants/notifications")
def get_applicants_notifications(id: int):
    return handle_get_applicants_notifications(id)


@routes.get("/applicants/{id}/exams")
def get_applicants_exams(id: int):
    return handle_get_applicants_exams(id)


@routes.post("/applicants/{id}/exams")
def post_applicants_exams(id: int, applicant_exam: ApplicantsExams):
    return handle_post_applicants_exams(id, applicant_exam)


@routes.post("/applicants/send-feedback-email")
def post_send_feedback_email(body: SendFeedbackEmailBody):
    return handle_post_send_feedback_email(body)


@routes.get("/applicants/{id}/redirected-to")
def get_applicants_redirect_to(id: int):
    return handle_get_applicants_redirected_to(id)


@routes.post("/applicants/redirected-to")
def post_applicants_redirect_to(body: RedirectedTo):
    return handle_post_applicants_redirected_to(body)


@routes.get("/applicant-process/{applicant_id}")
def get_applicant_process(applicant_id: int):
    return handle_get_applicant_process(applicant_id)


@routes.put("/applicant-process/{applicant_id}")
def upsert_applicant_process(applicant_id: int, applicant_process: ApplicantProcess):
    return handle_upsert_applicant_process(applicant_id, applicant_process)


@routes.get("/applicants-docs/{applicant_id}")
def get_applicant_docs_by_applicant_id(applicant_id: int):
    return handle_get_applicant_docs_by_applicant_id(applicant_id)


@routes.get("/applicants-docs/file/{id}/{doc_type}")
def get_document_file_by_id(id: int, doc_type: str):
    return handle_get_document_file_by_id(id, doc_type)


@routes.post("/applicants-docs/{applicant_id}")
def post_applicants_docs(
    applicant_id: int,
    resume: UploadFile = File(...),
    workcard: UploadFile = File(...),
):
    return handle_post_applicants_docs(applicant_id, resume, workcard)
