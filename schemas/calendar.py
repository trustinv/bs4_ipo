import re
from datetime import datetime

from pydantic import BaseModel, validator, Field


class CalendarBaseSchema(BaseModel):
    ac_sdate: str = ""
    ac_edate: str = ""
    ac_category_name: str = ""
    ac_category: int = 0
    ac_company_name: str = ""
    ac_vitalize: str = "Y"
    ac_datetime: datetime = datetime.now()


class CalendarCreateSchema(CalendarBaseSchema):
    @validator("ac_sdate", pre=True)
    def convert_ac_sdate(cls, value):
        value = value.replace(" ", "").replace("/", "-").strip()
        return value

    @validator("ac_edate", pre=True)
    def convert_ac_edate(cls, value):
        value = value.replace(" ", "").replace("/", "-").strip()
        return value

    @validator("ac_category", pre=True)
    def convert_ac_category(cls, value):
        return value

    @validator("ac_category_name", pre=True)
    def convert_ac_category_name(cls, value):
        return value

    @validator("ac_company_name", pre=True)
    def convert_ac_company_name(cls, value):
        return value


class CalendarSchema(BaseModel):
    ac_idx: int = Field(..., title="AC Idx", description="AC Idx")
    ci_idx: int = Field(..., title="CI Idx", description="CI Idx")

    class Config:
        orm_mode = True
