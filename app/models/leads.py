import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, Uuid, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON

from app.db import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    partner_id = Column(Uuid, ForeignKey("partners.id"), nullable=False)
    offer_id = Column(Uuid, ForeignKey("offers.id", ondelete="RESTRICT"), nullable=False)
    status = Column(String, nullable=False)
    contact_json = Column(JSON, nullable=False)
    notes = Column(String)
    source = Column(String)
    assigned_to_user_id = Column(Uuid, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    routed_at = Column(DateTime(timezone=True))
    routing_result_json = Column(JSON)

    events = relationship("LeadEvent", back_populates="lead", cascade="all, delete-orphan")


class LeadEvent(Base):
    __tablename__ = "lead_events"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    lead_id = Column(Uuid, ForeignKey("leads.id", ondelete="CASCADE"), nullable=False)
    event_type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False, server_default="{}")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    lead = relationship("Lead", back_populates="events")
