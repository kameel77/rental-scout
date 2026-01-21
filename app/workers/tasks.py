from app.db import SessionLocal
from app.services.importer import process_import_batch
from app.workers.celery_app import celery_app


@celery_app.task(name="imports.process_batch")
def process_import_task(batch_id: str, file_path: str, adapter_type: str, program_code: str | None = None):
    db = SessionLocal()
    try:
        return process_import_batch(db, batch_id, file_path, adapter_type, program_code=program_code)
    finally:
        db.close()
