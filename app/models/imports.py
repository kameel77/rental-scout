import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Uuid, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON

from app.db import Base


class ImportBatch(Base):
    __tablename__ = "import_batches"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    partner_id = Column(Uuid, ForeignKey("partners.id"), nullable=False)
    source_filename = Column(String, nullable=False)
    source_file_hash = Column(String, nullable=False)
    uploaded_by_user_id = Column(Uuid, ForeignKey("users.id"))
    status = Column(String, nullable=False)
    rows_total = Column(Integer, nullable=False, server_default="0")
    rows_success = Column(Integer, nullable=False, server_default="0")
    rows_failed = Column(Integer, nullable=False, server_default="0")
    errors_json = Column(JSON)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    parsed_at = Column(DateTime(timezone=True))

    rows = relationship("ImportRow", back_populates="import_batch", cascade="all, delete-orphan")


class ImportRow(Base):
    __tablename__ = "import_rows"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    import_batch_id = Column(Uuid, ForeignKey("import_batches.id", ondelete="CASCADE"), nullable=False)
    row_number = Column(Integer, nullable=False)
    raw_row = Column(JSON, nullable=False)
    normalized_row = Column(JSON)
    status = Column(String, nullable=False)
    error_message = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    import_batch = relationship("ImportBatch", back_populates="rows")
