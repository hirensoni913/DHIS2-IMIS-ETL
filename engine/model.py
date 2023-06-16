from winreg import QueryInfoKey
from typing import Optional

from pydantic import BaseModel
from type import *


class Integration:
    def __init__(self, query: str, parameters: dict, description: str) -> None:
        self.description = description
        self.query = query
        self.parameters = parameters


class Metadata(BaseModel):
    id: Optional[uid]
    name: str230
    code: Optional[str50]


class OrganisationUnit(Metadata):
    shortName: str50 = ''
    openingDate: dateStr
    parent: Optional[DHIS2Ref]
