from fastapi import APIRouter, Depends

from controllers.applicants import (
    handle_delete_applicants,
    handle_get_applicants,
    handle_get_applicants_exams,
    handle_get_applicants_notifications,
    handle_patch_applicants,
    handle_post_applicant,
    handle_post_applicants_exams,
    handle_post_hire_applicants,
    handle_post_send_feedback_email,
)
from functions.auth import verify_token
from models.applicants import Applicants
from models.applicants_exams import ApplicantsExams
from pyhints.applicants import RecruitProps, SendFeedbackEmailBody

routes = APIRouter(dependencies=[Depends(verify_token)])


@routes.get("/applicants")
def get_applicants():
    return handle_get_applicants()


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
