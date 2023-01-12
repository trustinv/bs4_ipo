import re
from datetime import datetime

from pydantic import BaseModel, validator, Field
from utilities import converters


class PredictionBaseSchema(BaseModel):

    ci_price: str = ""
    ci_incidence: int = 0
    ci_incidence_specific_gravity: float = 0.0
    ci_participation: int = 0
    ci_participation_specific_gravity: float = 0.0
    ci_datetime: datetime = datetime.now()


class PredictionCreateSchema(PredictionBaseSchema):
    @validator("ci_price", pre=True)
    def convert_ci_price(cls, value):
        if isinstance(value, str):
            value = value.strip()
            return value
        return value

    @validator("ci_incidence", pre=True)
    def convert_ci_incidence(cls, value):
        if isinstance(value, str):
            value = int(converters.only_digits(value))
            return value
        return value

    @validator("ci_participation", pre=True)
    def convert_ci_participation(cls, value):
        if isinstance(value, str):
            value = int(converters.only_digits(value))
            return value
        return value

    @validator("ci_incidence_specific_gravity", pre=True)
    def convert_ci_incidence_specific_gravity(cls, value):
        return converters.only_digits_to_float(value)

    @validator("ci_participation_specific_gravity", pre=True)
    def convert_ci_participation_specific_gravity(cls, value):
        return converters.only_digits_to_float(value)


class PredictionSchema(PredictionBaseSchema):

    cip_idx: int = Field(..., title="AC Idx", description="CIP Idx")
    ci_idx: int = Field(..., title="CI Idx", description="CI Idx")

    class Config:
        orm_mode = True
