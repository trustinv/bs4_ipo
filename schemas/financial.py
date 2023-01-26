import re
from datetime import datetime

from pydantic import BaseModel, validator, Field
from utilities import converters


class FinancialBaseSchema(BaseModel):

    ci_category1: str = ""
    ci_category2: str = ""
    ci_current_asset: float = 0.0
    ci_non_current_asset: float = 0.0
    ci_current_liability: float = 0.0
    ci_non_current_liability: float = 0.0
    ci_capital: float = 0.0
    ci_capital_surplus: float = 0.0
    ci_earned_surplus: float = 0.0
    ci_other_capital_items: float = 0.0
    ci_turnover: float = 0.0
    ci_business_profits: float = 0.0
    ci_net_income: float = 0.0
    ci_eps: float = 0.0
    ci_datetime: datetime = datetime.now()


class FinancialCreateSchema(FinancialBaseSchema):
    @validator("ci_current_asset", pre=True)
    def convert_ci_current_asset(cls, value):
        return value

    @validator("ci_non_current_asset", pre=True)
    def convert_ci_non_current_asset(cls, value):
        return value

    @validator("ci_current_liability", pre=True)
    def convert_ci_current_liability(cls, value):
        return value

    @validator("ci_non_current_liability", pre=True)
    def convert_ci_non_current_liability(cls, value):
        return value

    @validator("ci_capital", pre=True)
    def convert_ci_capital(cls, value):
        if value == "0\xa0원":
            return 0.0
        else:
            value = float(value.split("원")[0].replace("\xa0", "").replace(" ", "").strip())
        return value

    @validator("ci_capital_surplus", pre=True)
    def convert_ci_capital_surplus(cls, value):
        return value

    @validator("ci_earned_surplus", pre=True)
    def convert_ci_earned_surplus(cls, value):
        return value

    @validator("ci_other_capital_items", pre=True)
    def convert_ci_other_capital_items(cls, value):
        return value

    @validator("ci_turnover", pre=True)
    def convert_ci_turnover(cls, value):
        return value

    @validator("ci_business_profits", pre=True)
    def convert_ci_business_profits(cls, value):
        return value

    @validator("ci_net_income", pre=True)
    def convert_ci_net_income(cls, value):
        return value

    @validator("ci_eps", pre=True)
    def convert_ci_eps(cls, value):
        return value


class FinancialSchema(FinancialBaseSchema):
    cif_idx: int = Field(..., title="CIF Idx", description="CIF Idx")
    ci_idx: int = Field(..., title="CI Idx", description="CI Idx")

    class Config:
        orm_mode = True
