from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import date

class Candidato(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    data_cadastro: date
    nome: str = Field(index=True)
    email: str = Field(index=True)
    telefone: str = Field(index=True)
    municipio: str = Field(index=True)
    cidade: str = Field(index=True)
    uf: str = Field(index=True)
    tempo_em_sc: int = Field(index=True)
    cargo: str = Field(index=True)
    experiencia: bool = Field(index=True)
    endereço: str = Field(index=True)
    bairro: str = Field(index=True)
    cep: str = Field(index=True)
    sugestao_unidade: str = Field(index=True)
    data_nascimento: date
    nome_pai: str = Field(index=True)
    nome_mae: str = Field(index=True)
    escolaridade: str = Field(index=True)
    estado_civil: str = Field(index=True)
    sexo: str = Field(index=True)
    ultimo_salario: float = Field(index=True)
    Cedula_identidade: str = Field(index=True)
    cpf: str = Field(index=True)
    cnh: str = Field(index=True)
    Filhos: int = Field(index=True)
    indicado_por: str = Field(index=True)
    tipo_residencia: str = Field(index=True)
    meio_transporte: str = Field(index=True)
    ultima_remuneração: float = Field(index=True)
    ultima_empresa: str = Field(index=True)
    ultima_função: str = Field(index=True)
    ultima_data_admissão: date
    ultima_data_demissão: date
    motivo_desligamento_ultima: str = Field(index=True)
    ultima_penultima_empresa: str = Field(index=True)
    ultima_penultima_função: str = Field(index=True)
    ultima_penultima_data_admissão: date
    ultima_penultima_data_demissão: date
    motivo_desligamento_penultima: str = Field(index=True)
    ultima_ante_penultima_empresa: str = Field(index=True)
    ultima_ante_penultima_função: str = Field(index=True)
    ultima_ante_penultima_data_admissão: date
    ultima_ante_penultima_data_demissão: date
    motivo_desligamento_ante_penultima: str = Field(index=True)
    apresentação_pessoal: str = Field(index=True)
    comunicativo: str = Field(index=True)
    postura: str = Field(index=True)
    simpatia: str = Field(index=True)
    observacoes: str = Field(index=True)
    aprovado: str = Field(index=True)
    primeira_entrevista: str = Field(index=True)
    data_encaminhamento_segunda_entrevista: date
    horario_segunda_entrevista: str = Field(index=True) 
    unidade_de_negocio: str = Field(index=True)
    encaminhado_para_admissao: str = Field(index=True)
    data_encaminhamento_admissao: date
    data_prevista_admissao: date  
    unidade_de_negocio_admissao: str = Field(index=True)
    horario_trabalho: str = Field(index=True)