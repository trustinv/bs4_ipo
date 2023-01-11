import re
from datetime import datetime

from pydantic import BaseModel, validator, Field
from utilities import converters


class SubscriberBaseSchema(BaseModel):

    ci_stock_firm: str = ""
    ci_assign_quantity: int = 0
    ci_limit: int = 0
    ci_note: str = ""
    ci_datetime: datetime = datetime.now()


class SubscriberCreateSchema(SubscriberBaseSchema):
    @validator("ci_stock_firm", pre=True)
    def convert_ci_stock_firm(cls, value):
        value = value[:2]
        return value

    @validator("ci_assign_quantity", pre=True)
    def convert_ci_assign_quantity(cls, value):
        value = int(converters.only_digits(value))
        return value

    @validator("ci_limit", pre=True)
    def convert_ci_limit(cls, value):
        value = int(converters.only_digits(value))
        return value

    @validator("ci_note", pre=True)
    def convert_ci_note(cls, value):
        return value.strip()


class CompanyInfoSubscriberSchema(SubscriberBaseSchema):
    cis_idx: int = Field(..., title="CIS Idx", description="CIS Idx")
    ci_idx: int = Field(..., title="CI Idx", description="CI Idx")

    class Config:
        orm_mode = True
