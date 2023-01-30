import re
from datetime import datetime

from pydantic import BaseModel, validator, Field
from utilities import converters


class ShareholderBase(BaseModel):

    ci_category: int = 0
    ci_category_name: str = ""
    ci_normal_stocks: int = 0
    ci_first_stocks: int = 0
    ci_share_rate: float = 0.0
    ci_protection_date: str = ""
    ci_datetime: datetime = datetime.now()


class ShareholderCreateSchema(ShareholderBase):
    @validator("ci_category", pre=True)
    def convert_ci_category(cls, value):
        return value

    @validator("ci_category_name", pre=True)
    def convert_ci_category_name(cls, value):
        return converters.remove_whitespace(value)

    @validator("ci_normal_stocks", pre=True)
    def convert_ci_normal_stocks(cls, value):
        value = converters.only_digits(value)
        return value

    @validator("ci_first_stocks", pre=True)
    def convert_ci_first_stocks(cls, value):
        value = converters.only_digits_to_int(value)
        return value

    @validator("ci_share_rate", pre=True)
    def convert_ci_share_rate(cls, value):
        value = converters.string_percentage_to_float(value)
        return value

    @validator("ci_protection_date", pre=True)
    def convert_ci_protection_date(cls, value):
        value = value.strip()
        return value


class ShareholderSchema(ShareholderBase):
    cis_idx: int = Field(..., title="CIS Idx", description="CIS Idx")
    ci_idx: int = Field(..., title="CI Idx", description="CI Idx")

    class Config:
        orm_mode = True
