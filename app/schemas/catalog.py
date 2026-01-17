from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class VehicleImageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    storage_key: str
    public_url: str
    sort_order: int
    alt: str | None = None
    is_cover: bool


class VehicleFeatures(BaseModel):
    audio_multimedia: list[str] = []
    comfort_extras: list[str] = []
    driver_assistance: list[str] = []
    performance_tuning: list[str] = []
    safety: list[str] = []


class VehicleSpec(BaseModel):
    category: str | None = None
    fuel: str | None = None
    transmission: str | None = None
    drive: str | None = None
    displacement: int | None = None
    seats: int | None = None
    doors: int | None = None
    power: int | None = None
    features: VehicleFeatures = VehicleFeatures()


class VehicleCatalogBase(BaseModel):
    title: str
    make: str
    model: str
    trim: str | None = None
    year: int | None = None
    description: str | None = None
    spec_json: VehicleSpec = VehicleSpec()
    color: str | None = None
    price_catalog: int | None = None
    promotion_options: list[str] = []
    is_published: bool = False


class VehicleCatalogCreate(VehicleCatalogBase):
    pass


class VehicleCatalogUpdate(BaseModel):
    title: str | None = None
    make: str | None = None
    model: str | None = None
    trim: str | None = None
    year: int | None = None
    description: str | None = None
    spec_json: VehicleSpec | None = None
    color: str | None = None
    price_catalog: int | None = None
    promotion_options: list[str] | None = None
    is_published: bool | None = None


class VehicleCatalogOut(VehicleCatalogBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime | None = None
    images: list[VehicleImageOut] = []


class VehicleLinkOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    vehicle_catalog_id: UUID
    calc_vehicle_id: UUID
    match_confidence: int | None = None
    created_at: datetime
