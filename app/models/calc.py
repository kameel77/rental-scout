import uuid

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, String, Uuid, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON

from app.db import Base


class CalcProgram(Base):
    __tablename__ = "calc_programs"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    partner_id = Column(Uuid, ForeignKey("partners.id"), nullable=False)
    code = Column(String, nullable=False)
    name = Column(String)
    valid_from = Column(Date)
    valid_to = Column(Date)
    currency = Column(String, nullable=False, server_default="PLN")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class CalcVehicle(Base):
    __tablename__ = "calc_vehicles"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    partner_id = Column(Uuid, ForeignKey("partners.id"), nullable=False)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    trim = Column(String)
    full_name = Column(String)
    external_model_key = Column(String)
    meta = Column(JSON, nullable=False, server_default="{}")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class CalcLine(Base):
    __tablename__ = "calc_lines"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    partner_id = Column(Uuid, ForeignKey("partners.id"), nullable=False)
    calc_program_id = Column(Uuid, ForeignKey("calc_programs.id", ondelete="CASCADE"), nullable=False)
    import_batch_id = Column(Uuid, ForeignKey("import_batches.id", ondelete="RESTRICT"), nullable=False)
    calc_vehicle_id = Column(Uuid, ForeignKey("calc_vehicles.id", ondelete="RESTRICT"), nullable=False)
    term_months = Column(Integer, nullable=False)
    annual_mileage_km = Column(Integer, nullable=False)
    total_mileage_km = Column(Integer, nullable=False)
    list_price_gross = Column(Numeric)
    discounted_price_gross = Column(Numeric)
    discount_pct = Column(Numeric)
    registration_fee_gross = Column(Numeric)
    rv_table = Column(String)
    rv_id = Column(String)
    rv_base_pct = Column(Numeric)
    rv_adj_pct = Column(Numeric)
    rv_pct = Column(Numeric)
    rv_amount = Column(Numeric)
    rm_table = Column(String)
    rm_id = Column(String)
    rm_val = Column(Numeric)
    rm_val_per_km = Column(Numeric)
    rm_amount = Column(Numeric)
    amortization_amount = Column(Numeric)
    book_value_y1 = Column(Numeric)
    book_value_y2 = Column(Numeric)
    book_value_y3 = Column(Numeric)
    book_value_y4 = Column(Numeric)
    raw_row = Column(JSON, nullable=False, server_default="{}")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    components = relationship("CalcCostComponent", back_populates="calc_line", cascade="all, delete-orphan")


class CalcCostComponent(Base):
    __tablename__ = "calc_cost_components"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    calc_line_id = Column(Uuid, ForeignKey("calc_lines.id", ondelete="CASCADE"), nullable=False)
    component_code = Column(String, nullable=False)
    label = Column(String, nullable=False)
    amount = Column(Numeric)
    unit = Column(String, nullable=False)
    meta = Column(JSON, nullable=False, server_default="{}")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    calc_line = relationship("CalcLine", back_populates="components")
