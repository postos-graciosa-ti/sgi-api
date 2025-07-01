from sqlmodel import Session, select

from database.sqlite import engine
from models.resignable_reasons import ResignableReasons


def demission_reasons():
    resignable_reasons = [
        {
            "name": "Demissão sem Justa Causa",
            "description": "Rescisão sem motivo específico por parte da empresa.",
        },
        {
            "name": "Demissão por Justa Causa",
            "description": "Rescisão devido a falta grave cometida pelo empregado.",
        },
        {
            "name": "Pedido de Demissão",
            "description": "Solicitação do empregado para encerrar o contrato de trabalho.",
        },
        {
            "name": "Pedido de Demissão Antecipada do Contrato de Experiência (parte empregado)",
            "description": "O empregado solicita o fim do contrato antes do prazo.",
        },
        {
            "name": "Demissão Antecipada do Contrato de Experiência (parte empresa)",
            "description": "A empresa decide encerrar o contrato de experiência antes do prazo.",
        },
        {
            "name": "Demissão por Justa Causa",
            "description": "Rescisão por justa causa devido a conduta inapropriada do empregado.",
        },
    ]

    with Session(engine) as session:
        exist_resignable_reason = session.exec(select(ResignableReasons)).all()

        if not exist_resignable_reason:
            for resignable_reason in resignable_reasons:
                reason = ResignableReasons(
                    name=resignable_reason["name"],
                    description=resignable_reason["description"],
                )

                session.add(reason)

            session.commit()
