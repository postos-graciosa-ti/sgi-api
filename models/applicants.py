from datetime import date
from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select


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