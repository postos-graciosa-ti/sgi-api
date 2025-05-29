from fastapi import APIRouter, Depends

from controllers.applicants import (
    handle_delete_applicants,
    handle_get_applicants,
    handle_patch_applicants,
    handle_post_applicant,
    handle_post_hire_applicants,
)
from functions.auth import verify_token
from models.applicants import Applicants
from pyhints.applicants import RecruitProps

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
