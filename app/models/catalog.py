import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Uuid, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON

from app.db import Base


class VehicleCatalog(Base):
    __tablename__ = "vehicles_catalog"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    trim = Column(String)
    year = Column(Integer)
    description = Column(String)
    spec_json = Column(JSON, nullable=False, server_default="{}")
    is_published = Column(Boolean, nullable=False, server_default="false")
    created_by_user_id = Column(Uuid, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    images = relationship("VehicleImage", back_populates="vehicle", cascade="all, delete-orphan")
    links = relationship("VehicleLink", back_populates="vehicle", cascade="all, delete-orphan")


class VehicleImage(Base):
    __tablename__ = "vehicle_images"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    vehicle_catalog_id = Column(Uuid, ForeignKey("vehicles_catalog.id", ondelete="CASCADE"), nullable=False)
    storage_key = Column(String, nullable=False)
    public_url = Column(String, nullable=False)
    sort_order = Column(Integer, nullable=False, server_default="0")
    alt = Column(String)
    is_cover = Column(Boolean, nullable=False, server_default="false")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    vehicle = relationship("VehicleCatalog", back_populates="images")


class VehicleLink(Base):
    __tablename__ = "vehicle_links"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    vehicle_catalog_id = Column(Uuid, ForeignKey("vehicles_catalog.id", ondelete="CASCADE"), nullable=False)
    calc_vehicle_id = Column(Uuid, ForeignKey("calc_vehicles.id", ondelete="RESTRICT"), nullable=False)
    match_confidence = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    vehicle = relationship("VehicleCatalog", back_populates="links")
