import os
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage
from typing import Optional

from dateutil.relativedelta import relativedelta
from fastapi import HTTPException
from sqlalchemy import and_, create_engine, event, text
from sqlmodel import Session, select

from database.sqlite import engine
from models.applicants import Applicants
from models.applicants_exams import ApplicantsExams
from models.function import Function
from models.redirected_to import RedirectedTo
from models.workers import Workers
from pyhints.applicants import RecruitProps, SendFeedbackEmailBody

# applicants


def handle_get_applicants():
    with Session(engine) as session:
        applicants = session.exec(
            select(Applicants)
            .where(Applicants.is_active == True)
            .order_by(Applicants.id.desc())
        ).all()

        return applicants


def handle_post_applicant(applicant: Applicants):
    with Session(engine) as session:
        session.add(applicant)

        session.commit()

        session.refresh(applicant)

        return applicant


def handle_patch_applicants(id: int, applicant: Applicants):
    with Session(engine) as session:
        db_applicant = session.exec(
            select(Applicants).where(Applicants.id == id)
        ).first()

        if applicant.redirect_to is not None:
            db_applicant.redirect_to = applicant.redirect_to

        if applicant.natural is not None:
            db_applicant.natural = applicant.natural

        if applicant.tempo is not None:
            db_applicant.tempo = applicant.tempo

        if applicant.vaga_interesse is not None:
            db_applicant.vaga_interesse = applicant.vaga_interesse

        if applicant.experiencia_funcao is not None:
            db_applicant.experiencia_funcao = applicant.experiencia_funcao

        if applicant.data_nascimento is not None:
            db_applicant.data_nascimento = applicant.data_nascimento

        if applicant.nome_pai is not None:
            db_applicant.nome_pai = applicant.nome_pai

        if applicant.nome_mae is not None:
            db_applicant.nome_mae = applicant.nome_mae

        if applicant.rg is not None:
            db_applicant.rg = applicant.rg

        if applicant.cpf is not None:
            db_applicant.cpf = applicant.cpf

        if applicant.estado_civil is not None:
            db_applicant.estado_civil = applicant.estado_civil

        if applicant.filhos is not None:
            db_applicant.filhos = applicant.filhos

        if applicant.fumante is not None:
            db_applicant.fumante = applicant.fumante

        if applicant.bairro is not None:
            db_applicant.bairro = applicant.bairro

        if applicant.onde_viu_vaga is not None:
            db_applicant.onde_viu_vaga = applicant.onde_viu_vaga

        if applicant.indicacao is not None:
            db_applicant.indicacao = applicant.indicacao

        if applicant.disponibilidade_horario is not None:
            db_applicant.disponibilidade_horario = applicant.disponibilidade_horario

        if applicant.moradia is not None:
            db_applicant.moradia = applicant.moradia

        if applicant.transporte is not None:
            db_applicant.transporte = applicant.transporte

        if applicant.ultimo_salario is not None:
            db_applicant.ultimo_salario = applicant.ultimo_salario

        if applicant.apresentacao_pessoal is not None:
            db_applicant.apresentacao_pessoal = applicant.apresentacao_pessoal

        if applicant.comunicativo is not None:
            db_applicant.comunicativo = applicant.comunicativo

        if applicant.postura is not None:
            db_applicant.postura = applicant.postura

        if applicant.simpatia is not None:
            db_applicant.simpatia = applicant.simpatia

        if applicant.observacoes is not None:
            db_applicant.observacoes = applicant.observacoes

        if applicant.sim_nao_talvez is not None:
            db_applicant.sim_nao_talvez = applicant.sim_nao_talvez

        if applicant.contato is not None:
            db_applicant.contato = applicant.contato

        if applicant.retorno_whatsapp is not None:
            db_applicant.retorno_whatsapp = applicant.retorno_whatsapp

        if applicant.primeira_entrevista is not None:
            db_applicant.primeira_entrevista = applicant.primeira_entrevista

        if applicant.segunda_entrevista is not None:
            db_applicant.segunda_entrevista = applicant.segunda_entrevista

        if applicant.encaminhado_admissional is not None:
            db_applicant.encaminhado_admissional = applicant.encaminhado_admissional

        if applicant.data_prevista_admissao is not None:
            db_applicant.data_prevista_admissao = applicant.data_prevista_admissao

        if applicant.filial is not None:
            db_applicant.filial = applicant.filial

        if applicant.horario is not None:
            db_applicant.horario = applicant.horario

        if applicant.is_aproved is not None:
            db_applicant.is_aproved = applicant.is_aproved

        if applicant.ultima_experiencia is not None:
            db_applicant.ultima_experiencia = applicant.ultima_experiencia

        if applicant.penultima_experiencia is not None:
            db_applicant.penultima_experiencia = applicant.penultima_experiencia

        if applicant.antepenultima_experiencia is not None:
            db_applicant.antepenultima_experiencia = applicant.antepenultima_experiencia

        if applicant.escolaridade is not None:
            db_applicant.escolaridade = applicant.escolaridade

        if applicant.rh_opinion is not None:
            db_applicant.rh_opinion = applicant.rh_opinion

        if applicant.coordinator_opinion is not None:
            db_applicant.coordinator_opinion = applicant.coordinator_opinion

        if applicant.special_notation is not None:
            db_applicant.special_notation = applicant.special_notation

        if applicant.coordinator_observations is not None:
            db_applicant.coordinator_observations = applicant.coordinator_observations

        if applicant.attendance_date is not None:
            db_applicant.attendance_date = applicant.attendance_date

        if applicant.is_active is not None:
            db_applicant.is_active = applicant.is_active

        if applicant.email is not None:
            db_applicant.email = applicant.email

        if applicant.mobile is not None:
            db_applicant.mobile = applicant.mobile

        if applicant.whatsapp_feedback is not None:
            db_applicant.whatsapp_feedback = applicant.whatsapp_feedback

        session.add(db_applicant)

        session.commit()

        session.refresh(db_applicant)

        return db_applicant


def handle_delete_applicants(id: int):
    with Session(engine) as session:
        db_applicant = session.exec(
            select(Applicants).where(Applicants.id == id)
        ).first()

        session.delete(db_applicant)

        session.commit()

        return {"success": True}


# hire applicants


def get_civil_status_id(estado_civil: Optional[str]) -> Optional[int]:
    if not estado_civil:
        return None

    civil_status_map = {
        "solteiro": 1,
        "casado": 2,
        "divorciado": 3,
        "viúvo": 4,
        "separado": 5,
    }

    return civil_status_map.get(estado_civil.lower(), 1)


def get_school_level_id(escolaridade: Optional[str]) -> Optional[int]:
    if not escolaridade:
        return None

    school_level_map = {
        "fundamental incompleto": 1,
        "fundamental completo": 2,
        "médio incompleto": 3,
        "médio completo": 4,
        "superior incompleto": 5,
        "superior completo": 6,
        "pós-graduação": 7,
        "mestrado": 8,
        "doutorado": 9,
    }

    return school_level_map.get(escolaridade.lower(), 1)


def handle_post_hire_applicants(recruit: RecruitProps) -> Optional[Workers]:
    with Session(engine) as session:
        db_applicant = session.exec(
            select(Applicants).where(Applicants.id == recruit.applicant_id)
        ).first()

        if not db_applicant:
            raise ValueError(f"Applicant with ID {recruit.applicant_id} not found")

        new_worker = Workers(
            name=db_applicant.name,
            cpf=db_applicant.cpf,
            rg=db_applicant.rg,
            rg_issuing_agency="",
            rg_expedition_date=db_applicant.data_nascimento,
            fathername=db_applicant.nome_pai,
            mothername=db_applicant.nome_mae,
            birthdate=db_applicant.data_nascimento,
            email=db_applicant.email,
            mobile=db_applicant.contato or db_applicant.mobile,
            phone=db_applicant.contato,
            emergency_number=db_applicant.contato,
            bairro=db_applicant.bairro,
            street="",
            street_number="",
            street_complement="",
            cep="",
            experience_time=db_applicant.experiencia_funcao,
            previous_experience=True if db_applicant.experiencia_funcao else False,
            ultima_experiencia=db_applicant.ultima_experiencia,
            penultima_experiencia=db_applicant.penultima_experiencia,
            antepenultima_experiencia=db_applicant.antepenultima_experiencia,
            admission_date=datetime.now().strftime("%Y-%m-%d"),
            resignation_date=datetime.now().strftime("%Y-%m-%d"),
            first_review_date=(datetime.now() + relativedelta(months=1)).strftime(
                "%Y-%m-%d"
            ),
            second_review_date=(datetime.now() + relativedelta(months=2)).strftime(
                "%Y-%m-%d"
            ),
            last_function_date=datetime.now().strftime("%Y-%m-%d"),
            wage=db_applicant.ultimo_salario,
            has_children=(
                True
                if db_applicant.filhos and db_applicant.filhos.lower() == "sim"
                else False
            ),
            children_data="[]",
            pis="",
            ctps="",
            ctps_serie="",
            ctps_emission_date="",
            rh_opinion=db_applicant.rh_opinion,
            coordinator_opinion=db_applicant.coordinator_opinion,
            special_notation=db_applicant.special_notation,
            coordinator_observations=db_applicant.coordinator_observations,
            is_active=True,
            is_away=False,
            first_job=False if db_applicant.experiencia_funcao else True,
            was_employee=True if db_applicant.experiencia_funcao else False,
            subsidiarie_id=1,
            function_id=1,
            cost_center_id=1,
            department_id=1,
            turn_id=1,
            civil_status_id=get_civil_status_id(db_applicant.estado_civil),
            school_level=get_school_level_id(db_applicant.escolaridade),
            ethnicity_id=1,
            gender_id=1,
            neighborhood_id=1,
            city=1,
            state=1,
            bank=1,
            wage_payment_method=1,
            enrolment="",
            esocial="",
            cbo="",
            general_function_code="",
            picture="",
            timecode="",
            sales_code="",
            votant_title="",
            votant_zone="",
            votant_session="",
            cnh="",
            cnh_emition_date="",
            cnh_valid_date="",
            cnh_category=1,
            union_contribute_current_year=False,
            receiving_unemployment_insurance=False,
            month_wage=db_applicant.ultimo_salario,
            hour_wage="",
            journey_wage="",
            transport_voucher="",
            transport_voucher_quantity="",
            diary_workjourney="",
            week_workjourney="",
            month_workjourney="",
            nocturne_hours="",
            dangerousness=False,
            unhealthy=False,
            early_payment=False,
            harmfull_exposition=False,
            has_experience_time=True if db_applicant.experiencia_funcao else False,
            has_nocturne_hours=False,
            propotional_payment=False,
            total_nocturne_workjourney="",
            twenty_five_workjourney="",
            twenty_two_to_five_week_workjourney="",
            twenty_two_to_five_month_workjourney="",
            twenty_two_to_five_effective_diary_workjourney="",
            healthcare_plan=False,
            healthcare_plan_discount="",
            life_insurance=False,
            life_insurance_discount="",
            ag="",
            cc="",
            early_payment_discount="",
        )

        session.add(new_worker)

        session.commit()

        session.refresh(new_worker)

        session.delete(db_applicant)

        session.commit()

        return new_worker


def handle_get_applicants_notifications(id: int):
    with Session(engine) as session:
        query = text(
            """
            SELECT *
            FROM applicants
            WHERE redirect_to = :user_id
              AND (coordinator_observation IS NULL OR coordinator_observation = '')
            """
        )

        result = session.exec(query.params(user_id=id)).mappings().all()

        return result


def handle_get_applicants_exams(id: int):
    with Session(engine) as session:
        applicants_exams = session.exec(
            select(ApplicantsExams).where(ApplicantsExams.applicant_id == id)
        ).all()

        return applicants_exams


def handle_post_applicants_exams(id: int, applicant_exam: ApplicantsExams):
    applicant_exam.applicant_id = id

    with Session(engine) as session:
        session.add(applicant_exam)

        session.commit()

        session.refresh(applicant_exam)

        return {"success": True}


def handle_post_send_feedback_email(body: SendFeedbackEmailBody):
    with Session(engine) as session:
        db_applicant = session.exec(
            select(Applicants).where(Applicants.id == body.id)
        ).first()

        if not db_applicant:
            raise HTTPException(status_code=404, detail="Candidato não encontrado")

        EMAIL_REMETENTE = os.environ.get("EMAIL_REMETENTE")

        SENHA = os.environ.get("SENHA")

        BCC = os.environ.get("BCC")

        if not all([EMAIL_REMETENTE, SENHA, BCC]):
            raise HTTPException(
                status_code=500, detail="Configuração de e-mail incompleta"
            )

        msg = EmailMessage()

        msg["Subject"] = f"Retorno de entrevista de {body.name}"

        msg["From"] = EMAIL_REMETENTE

        msg["To"] = body.email

        msg["Bcc"] = BCC

        msg.set_content(body.message)

        try:
            with open("assets/lista_de_documentos.pdf", "rb") as f:
                msg.add_attachment(
                    f.read(),
                    maintype="application",
                    subtype="pdf",
                    filename="lista_de_documentos.pdf",
                )

        except FileNotFoundError:
            raise HTTPException(status_code=500, detail="Arquivo PDF não encontrado")

        db_applicant.email_feedback = "sim"

        session.add(db_applicant)

        session.commit()

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_REMETENTE, SENHA)

                smtp.send_message(msg)

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Erro ao enviar e-mail: {str(e)}"
            )

        return {"message": "E-mail enviado com sucesso"}


def handle_get_applicants_redirected_to(id: int):
    with Session(engine) as session:
        result = session.exec(
            select(RedirectedTo).where(RedirectedTo.applicant_id == id)
        ).first()

        return result


def handle_post_applicants_redirected_to(body: RedirectedTo):
    with Session(engine) as session:
        session.add(body)

        session.commit()

        session.refresh(body)

        return {"success": True}
