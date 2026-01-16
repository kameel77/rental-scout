from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class APIModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class IDModel(APIModel):
    id: UUID


class TimestampedModel(APIModel):
    created_at: datetime


class JSONModel(APIModel):
    data: dict[str, Any]
