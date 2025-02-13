import logging
from functools import wraps
from typing import Any, Callable, TypeVar

from fastapi import HTTPException
from sqlalchemy.exc import MultipleResultsFound, NoResultFound, SQLAlchemyError

logging.basicConfig(level=logging.ERROR)

logger = logging.getLogger(__name__)

T = TypeVar("T")


def handle_database_query(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> T:
        try:
            return await func(*args, **kwargs)

        except NoResultFound:
            raise HTTPException(
                status_code=404, detail="Resource not found with the given parameters"
            )

        except MultipleResultsFound:
            raise HTTPException(
                status_code=500, detail="Unexpected multiple results found"
            )

        except SQLAlchemyError as e:
            logger.error(f"Database error: {str(e)}")

            raise HTTPException(
                status_code=500,
                detail="An error occurred while processing your request",
            )

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")

            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred. Please try again later",
            )

    return wrapper
