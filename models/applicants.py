from typing import Optional

from sqlmodel import Field, SQLModel


class Applicants(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None, nullable=True)
    natural: Optional[str] = Field(default=None, nullable=True)
    tempo: Optional[str] = Field(default=None, nullable=True)
    vaga_interesse: Optional[str] = Field(default=None, nullable=True)
    experiencia_funcao: Optional[str] = Field(default=None, nullable=True)
    data_nascimento: Optional[str] = Field(default=None, nullable=True)
    nome_pai: Optional[str] = Field(default=None, nullable=True)
    nome_mae: Optional[str] = Field(default=None, nullable=True)
    rg: Optional[str] = Field(default=None, nullable=True)
    cpf: Optional[str] = Field(default=None, nullable=True)
    estado_civil: Optional[str] = Field(default=None, nullable=True)
    filhos: Optional[str] = Field(default=None, nullable=True)
    fumante: Optional[str] = Field(default=None, nullable=True)
    bairro: Optional[str] = Field(default=None, nullable=True)
    onde_viu_vaga: Optional[str] = Field(default=None, nullable=True)
    indicacao: Optional[str] = Field(default=None, nullable=True)
    disponibilidade_horario: Optional[str] = Field(default=None, nullable=True)
    moradia: Optional[str] = Field(default=None, nullable=True)
    transporte: Optional[str] = Field(default=None, nullable=True)
    ultimo_salario: Optional[str] = Field(default=None, nullable=True)
    apresentacao_pessoal: Optional[str] = Field(default=None, nullable=True)
    comunicativo: Optional[str] = Field(default=None, nullable=True)
    postura: Optional[str] = Field(default=None, nullable=True)
    simpatia: Optional[str] = Field(default=None, nullable=True)
    observacoes: Optional[str] = Field(default=None, nullable=True)
    sim_nao_talvez: Optional[str] = Field(default=None, nullable=True)
    contato: Optional[str] = Field(default=None, nullable=True)
    retorno_whatsapp: Optional[str] = Field(default=None, nullable=True)
    primeira_entrevista: Optional[str] = Field(default=None, nullable=True)
    segunda_entrevista: Optional[str] = Field(default=None, nullable=True)
    encaminhado_admissional: Optional[str] = Field(default=None, nullable=True)
    data_prevista_admissao: Optional[str] = Field(default=None, nullable=True)
    filial: Optional[str] = Field(default=None, nullable=True)
    horario: Optional[str] = Field(default=None, nullable=True)
    created_by: Optional[int] = Field(
        default=None, nullable=True, foreign_key="user.id", index=True
    )
    redirect_to: Optional[int] = Field(
        default=None, nullable=True, foreign_key="user.id", index=True
    )
    is_aproved: Optional[bool] = Field(default=False)

    ultima_experiencia: Optional[str] = Field(default=None, nullable=True)
    penultima_experiencia: Optional[str] = Field(default=None, nullable=True)
    antepenultima_experiencia: Optional[str] = Field(default=None, nullable=True)
    escolaridade: Optional[str] = Field(default=None, nullable=True)
    rh_opinion: Optional[str] = Field(default=None, nullable=True)
    coordinator_opinion: Optional[str] = Field(default=None, nullable=True)
    special_notation: Optional[str] = Field(default=None, nullable=True)
    coordinator_observations: Optional[str] = Field(default=None, nullable=True)
    attendance_date: Optional[str] = Field(default=None, nullable=True)
    is_active: Optional[bool] = Field(default=True)
    email: Optional[str] = Field(default=None, nullable=True)
    feedback_status: Optional[str] = Field(default=None, nullable=True)
    mobile: Optional[str] = Field(default=None, nullable=True)
    email_feedback: Optional[str] = Field(default=None, nullable=True)
    whatsapp_feedback: Optional[str] = Field(default=None, nullable=True)

    rh_personal_life: Optional[str] = Field(default=None, nullable=True)
    rh_gas_station_experience: Optional[str] = Field(default=None, nullable=True)
    rh_life_structure: Optional[str] = Field(default=None, nullable=True)
    rh_working_here_objectives: Optional[str] = Field(default=None, nullable=True)
    rh_expect_working_here: Optional[str] = Field(default=None, nullable=True)
    rh_applicant_criteria: Optional[str] = Field(default=None, nullable=True)
    rh_wage_info: Optional[str] = Field(default=None, nullable=True)
    rh_target_goals: Optional[str] = Field(default=None, nullable=True)
    rh_claimed_goals: Optional[str] = Field(default=None, nullable=True)
    rh_client_fidelity: Optional[str] = Field(default=None, nullable=True)
    rh_hard_situations: Optional[str] = Field(default=None, nullable=True)
    rh_bad_reputation: Optional[str] = Field(default=None, nullable=True)
    rh_boring_consumer: Optional[str] = Field(default=None, nullable=True)
    rh_rage_at_workplace: Optional[str] = Field(default=None, nullable=True)
    rh_ecorp_changes: Optional[str] = Field(default=None, nullable=True)
    rh_team_work: Optional[str] = Field(default=None, nullable=True)
    rh_work_relationships: Optional[str] = Field(default=None, nullable=True)

    # coordinator interview questions

    personal_life: Optional[str] = Field(default=None, nullable=True)
    gas_station_experience: Optional[str] = Field(default=None, nullable=True)
    life_structure: Optional[str] = Field(default=None, nullable=True)
    working_here_objectives: Optional[str] = Field(default=None, nullable=True)
    expect_working_here: Optional[str] = Field(default=None, nullable=True)
    applicant_criteria: Optional[str] = Field(default=None, nullable=True)
    wage_info: Optional[str] = Field(default=None, nullable=True)

    target_goals: Optional[str] = Field(default=None, nullable=True)
    claimed_goals: Optional[str] = Field(default=None, nullable=True)
    client_fidelity: Optional[str] = Field(default=None, nullable=True)
    hard_situations: Optional[str] = Field(default=None, nullable=True)
    bad_reputation: Optional[str] = Field(default=None, nullable=True)
    boring_consumer: Optional[str] = Field(default=None, nullable=True)
    rage_at_workplace: Optional[str] = Field(default=None, nullable=True)
    ecorp_changes: Optional[str] = Field(default=None, nullable=True)
    team_work: Optional[str] = Field(default=None, nullable=True)
    work_relationships: Optional[str] = Field(default=None, nullable=True)

    work_experiences: Optional[str] = Field(default=None, nullable=True)

    picture_url: Optional[str] = Field(default=None, nullable=True)

    avaliation_complete: Optional[bool] = Field(default=False)
    identity_complete: Optional[bool] = Field(default=False)
    rh_interview_complete: Optional[bool] = Field(default=False)
    coordinator_interview_complete: Optional[bool] = Field(default=False)

    talents_database: int = Field(
        default=None, nullable=True, foreign_key="subsidiarie.id", index=True
    )
    talents_database_turn: int = Field(
        default=None, nullable=True, foreign_key="turn.id", index=True
    )
    talents_database_function: int = Field(
        default=None, nullable=True, foreign_key="function.id", index=True
    )

    selective_process_status: Optional[str] = Field(default=None, nullable=True)

    talents_bank_subsidiaries: Optional[str] = Field(default=None, nullable=True)
