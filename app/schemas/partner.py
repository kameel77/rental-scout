from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PartnerBase(BaseModel):
    name: str
    code: str
    workflow_key: str
    default_currency: str = "PLN"
    is_active: bool = True


class PartnerCreate(PartnerBase):
    pass


class PartnerUpdate(BaseModel):
    name: str | None = None
    workflow_key: str | None = None
    default_currency: str | None = None
    is_active: bool | None = None


class PartnerOut(PartnerBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime


class PartnerRoutingRuleBase(BaseModel):
    partner_id: UUID
    rule_name: str
    rule_json: dict[str, Any]
    target_json: dict[str, Any]
    is_active: bool = True


class PartnerRoutingRuleCreate(PartnerRoutingRuleBase):
    pass


class PartnerRoutingRuleUpdate(BaseModel):
    rule_name: str | None = None
    rule_json: dict[str, Any] | None = None
    target_json: dict[str, Any] | None = None
    is_active: bool | None = None


class PartnerRoutingRuleOut(PartnerRoutingRuleBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
