from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class DocsChecklist(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    worker_id: int = Field(foreign_key="workers.id")

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
