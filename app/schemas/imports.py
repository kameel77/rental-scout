from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ImportBatchOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    partner_id: UUID
    source_filename: str
    source_file_hash: str
    status: str
    rows_total: int
    rows_success: int
    rows_failed: int
    errors_json: dict[str, Any] | None = None
    uploaded_at: datetime
    parsed_at: datetime | None = None


class ImportBatchCreate(BaseModel):
    partner_id: UUID


class ImportRunResponse(BaseModel):
    task_id: str
