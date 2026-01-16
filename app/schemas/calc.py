from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CalcProgramBase(BaseModel):
    partner_id: UUID
    code: str
    name: str | None = None
    valid_from: date | None = None
    valid_to: date | None = None
    currency: str = "PLN"


class CalcProgramCreate(CalcProgramBase):
    pass


class CalcProgramUpdate(BaseModel):
    name: str | None = None
    valid_from: date | None = None
    valid_to: date | None = None
    currency: str | None = None


class CalcProgramOut(CalcProgramBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime


class CalcVehicleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    partner_id: UUID
    make: str
    model: str
    trim: str | None = None
    full_name: str | None = None
    external_model_key: str | None = None
    meta: dict
    created_at: datetime
