from datetime import date, datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OfferComponentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    component_code: str
    label: str
    amount_net: float | None = None
    amount_gross: float | None = None
    unit: str
    included: bool
    meta: dict[str, Any]


class OfferOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    partner_id: UUID
    calc_vehicle_id: UUID | None = None
    term_months: int
    annual_mileage_km: int
    total_mileage_km: int | None = None
    currency: str
    vat_rate: float | None = None
    upfront_fee_net: float | None = None
    upfront_fee_gross: float | None = None
    monthly_total_net: float | None = None
    monthly_total_gross: float | None = None
    valid_from: date | None = None
    valid_to: date | None = None
    notes: str | None = None
    created_at: datetime
    components: list[OfferComponentOut] = []
