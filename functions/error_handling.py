import logging
from functools import wraps
from typing import Callable

from fastapi import HTTPException
from sqlalchemy.exc import MultipleResultsFound, NoResultFound, SQLAlchemyError

logging.basicConfig(level=logging.ERROR)

logger = logging.getLogger(__name__)

# Decorador para capturar erros de banco de dados e outros erros inesperados
def error_handler(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except NoResultFound:
            # Erro: Nenhum resultado encontrado
            raise HTTPException(
                status_code=404, detail="Resource not found with the given parameters"
            )

        except MultipleResultsFound:
            # Erro: Múltiplos resultados encontrados quando se esperava um único
            raise HTTPException(status_code=500, detail="Unexpected multiple results found")

        except SQLAlchemyError as e:
            # Erro de banco de dados
            logger.error(f"Database error: {str(e)}")
            raise HTTPException(
                status_code=500, detail="An error occurred while processing your request"
            )

        except Exception as e:
            # Erro genérico para outros tipos de erro inesperados
            logger.error(f"Unexpected error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred. Please try again later",
            )

    return wrapper
