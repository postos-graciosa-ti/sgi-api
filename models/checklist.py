from typing import Optional

from sqlmodel import Field, SQLModel


class Checklist(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    worker_id: int = Field(index=True, unique=True)
    foto_3x4: bool = False
    conta_salario: bool = False
    cartao_ideal: bool = False
    cnh: bool = False
    vacina_filhos: bool = False
    rg: bool = False
    certidao_casamento: bool = False
    certidao_reservista: bool = False
    certificado_nr20: bool = False
    comprovante_endereco: bool = False
    escolaridade: bool = False
    escolaridade_filhos: bool = False
    cpf: bool = False
    cpf_dependentes: bool = False
    ctps: bool = False
    email_pessoal: bool = False
    aso: bool = False
    telefone_emergencia: bool = False
    pensao: bool = False
    pis: bool = False
    uniforme: bool = False
    cartao_banco_brasil: bool = False
    titulo_eleitor: bool = False


class ChecklistUpdate(SQLModel):
    worker_id: Optional[int]
    foto_3x4: Optional[bool]
    conta_salario: Optional[bool]
    cartao_ideal: Optional[bool]
    cnh: Optional[bool]
    vacina_filhos: Optional[bool]
    rg: Optional[bool]
    certidao_casamento: Optional[bool]
    certidao_reservista: Optional[bool]
    certificado_nr20: Optional[bool]
    comprovante_endereco: Optional[bool]
    escolaridade: Optional[bool]
    escolaridade_filhos: Optional[bool]
    cpf: Optional[bool]
    cpf_dependentes: Optional[bool]
    ctps: Optional[bool]
    email_pessoal: Optional[bool]
    aso: Optional[bool]
    telefone_emergencia: Optional[bool]
    pensao: Optional[bool]
    pis: Optional[bool]
    uniforme: Optional[bool]
    cartao_banco_brasil: Optional[bool]
    titulo_eleitor: Optional[bool]


class ChecklistCreate(SQLModel):
    worker_id: int
    foto_3x4: bool = False
    conta_salario: bool = False
    cartao_ideal: bool = False
    cnh: bool = False
    vacina_filhos: bool = False
    rg: bool = False
    certidao_casamento: bool = False
    certidao_reservista: bool = False
    certificado_nr20: bool = False
    comprovante_endereco: bool = False
    escolaridade: bool = False
    escolaridade_filhos: bool = False
    cpf: bool = False
    cpf_dependentes: bool = False
    ctps: bool = False
    email_pessoal: bool = False
    aso: bool = False
    telefone_emergencia: bool = False
    pensao: bool = False
    pis: bool = False
    uniforme: bool = False
    cartao_banco_brasil: bool = False
    titulo_eleitor: bool = False
