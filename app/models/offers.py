import uuid

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, Numeric, String, Uuid, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON

from app.db import Base


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    partner_id = Column(Uuid, ForeignKey("partners.id"), nullable=False)
    import_batch_id = Column(Uuid, ForeignKey("import_batches.id", ondelete="RESTRICT"), nullable=False)
    calc_line_id = Column(Uuid, ForeignKey("calc_lines.id", ondelete="SET NULL"))
    calc_vehicle_id = Column(Uuid, ForeignKey("calc_vehicles.id", ondelete="SET NULL"))
    external_offer_id = Column(String)
    term_months = Column(Integer, nullable=False)
    annual_mileage_km = Column(Integer, nullable=False)
    total_mileage_km = Column(Integer)
    currency = Column(String, nullable=False, server_default="PLN")
    vat_rate = Column(Numeric)
    upfront_fee_net = Column(Numeric)
    upfront_fee_gross = Column(Numeric)
    monthly_total_net = Column(Numeric)
    monthly_total_gross = Column(Numeric)
    valid_from = Column(Date)
    valid_to = Column(Date)
    notes = Column(String)
    raw_row = Column(JSON, nullable=False, server_default="{}")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    components = relationship("OfferComponent", back_populates="offer", cascade="all, delete-orphan")


class OfferComponent(Base):
    __tablename__ = "offer_components"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    offer_id = Column(Uuid, ForeignKey("offers.id", ondelete="CASCADE"), nullable=False)
    component_code = Column(String, nullable=False)
    label = Column(String, nullable=False)
    amount_net = Column(Numeric)
    amount_gross = Column(Numeric)
    unit = Column(String, nullable=False)
    included = Column(Boolean, nullable=False, server_default="true")
    meta = Column(JSON, nullable=False, server_default="{}")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    offer = relationship("Offer", back_populates="components")
