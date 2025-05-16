from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from sqlalchemy import and_, create_engine, event, text
from sqlmodel import Session, select

from database.sqlite import engine
from models.applicants import Applicants
from models.function import Function
from models.workers import Workers
from pyhints.applicants import RecruitProps

# applicants


def handle_get_applicants():
    with Session(engine) as session:
        applicants = session.exec(select(Applicants)).all()

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


def handle_post_hire_applicants(recruit: RecruitProps):
    with Session(engine) as session:
        worker = Workers(**recruit.worker_data)

        admission_date = datetime.strptime(worker.admission_date, "%Y-%m-%d").date()

        worker.first_review_date = (admission_date + relativedelta(months=1)).strftime(
            "%Y-%m-%d"
        )
        worker.second_review_date = (admission_date + relativedelta(months=2)).strftime(
            "%Y-%m-%d"
        )

        session.add(worker)

        session.commit()

        session.refresh(worker)

        applicant = session.exec(
            select(Applicants).where(Applicants.id == recruit.applicant_id)
        ).first()

        session.delete(applicant)

        session.commit()

        return worker


# applicants notifications


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
