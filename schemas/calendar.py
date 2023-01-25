import re
from datetime import datetime

from pydantic import BaseModel, validator, Field


class CalendarBaseSchema(BaseModel):
    ac_sdate: str = ""
    ac_edate: str = ac_sdate
    ac_category_name: str = ""
    ac_category: int = ac_category_name
    ac_company_name: str = ""
    ac_vitalize: str = 1
    ac_datetime: datetime = datetime.now()


class CalendarCreateSchema(CalendarBaseSchema):
    @validator("ac_sdate", pre=True)
    def convert_ac_sdate(cls, value):
        value = value.replace(" ", "").replace("/", "-").strip()
        return value

    @validator("ac_edate", pre=True)
    def convert_ac_edate(cls, value):
        end = value.replace(" ", "").replace("/", "-").strip()
        year = re.search(r"\d{4}", value)
        if year:
            year = year.group()
        e_date = f"{year}-{end}"
        return e_date

    @validator("ac_category", pre=True)
    def convert_ac_category(cls, value):
        if value == "ci_demand_forecast_date":
            return 1
        if value == "ci_public_subscription_date":
            return 2
        if value == "ci_refund_date":
            return 3
        if value == "ci_payment_date":
            return 4
        else:
            return 0

    @validator("ac_category_name", pre=True)
    def convert_ac_category_name(cls, value):
        if value == "ci_demand_forecast_date":
            return "수요예측일"
        if value == "ci_public_subscription_date":
            return "공모일"
        if value == "ci_refund_date":
            return "환불일"
        if value == "ci_payment_date":
            return "납입일"
        else:
            return ""

    @validator("ac_company_name", pre=True)
    def convert_ac_company_name(cls, value):
        return value.strip()


class CalendarSchema(BaseModel):
    ac_idx: int = Field(..., title="AC Idx", description="AC Idx")
    ci_idx: int = Field(..., title="CI Idx", description="CI Idx")

    class Config:
        orm_mode = True
