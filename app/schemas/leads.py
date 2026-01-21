from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class LeadCreate(BaseModel):
    offer_id: UUID
    contact_json: dict[str, Any]
    notes: str | None = None
    source: str | None = None


class LeadUpdate(BaseModel):
    status: str | None = None
    notes: str | None = None
    assigned_to_user_id: UUID | None = None


class LeadOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    partner_id: UUID
    offer_id: UUID
    status: str
    contact_json: dict[str, Any]
    notes: str | None = None
    source: str | None = None
    assigned_to_user_id: UUID | None = None
    created_at: datetime
    routed_at: datetime | None = None
    routing_result_json: dict[str, Any] | None = None
