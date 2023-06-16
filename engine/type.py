# dates
from typing import Optional
from pydantic import BaseModel, constr

# normal uid
uid = constr(regex="^[a-zA-Z][a-zA-Z0-9]{10}$")

# dates
dateStr = constr(regex="^\d{4}-\d{2}-\d{2}$")
datetimeStr = constr(regex="^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}$")

# string
str50 = constr(regex="^.{0,50}$")
str130 = constr(regex="^.{0,130}$")
str150 = constr(regex="^.{0,150}$")
str230 = constr(regex="^.{0,230}$")
str255 = constr(regex="^.{0,255}$")
period = constr(regex="^(?:[0-9]{4})|(?:[0-9]{6})|(?:[0-9]{8})$")


class DHIS2Ref(BaseModel):
    id: Optional[uid]
    code: Optional[str]
