import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Uuid, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON

from app.db import Base


class Partner(Base):
    __tablename__ = "partners"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)
    workflow_key = Column(String, nullable=False)
    default_currency = Column(String, nullable=False, server_default="PLN")
    is_active = Column(Boolean, nullable=False, server_default="true")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    routing_rules = relationship("PartnerRoutingRule", back_populates="partner", cascade="all, delete-orphan")


class PartnerRoutingRule(Base):
    __tablename__ = "partner_routing_rules"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    partner_id = Column(Uuid, ForeignKey("partners.id", ondelete="CASCADE"), nullable=False)
    rule_name = Column(String, nullable=False)
    rule_json = Column(JSON, nullable=False, server_default="{}")
    target_json = Column(JSON, nullable=False, server_default="{}")
    is_active = Column(Boolean, nullable=False, server_default="true")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    partner = relationship("Partner", back_populates="routing_rules")


class PartnerImportTemplate(Base):
    __tablename__ = "partner_import_templates"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    partner_id = Column(Uuid, ForeignKey("partners.id", ondelete="CASCADE"), nullable=False)
    template_type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    config_json = Column(JSON, nullable=False)
    is_active = Column(Boolean, nullable=False, server_default="true")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
