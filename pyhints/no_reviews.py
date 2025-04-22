from typing import List

from pydantic import BaseModel


class SubsidiaryFilter(BaseModel):
    subsidiaries_ids: List[int]
