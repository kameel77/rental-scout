from __future__ import annotations

import hashlib
import os
from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.db import get_db
from app.deps import get_current_user, require_role
from app.models import (
    CalcProgram,
    CalcVehicle,
    ImportBatch,
    Lead,
    Offer,
    Partner,
    PartnerRoutingRule,
    VehicleCatalog,
    VehicleImage,
    VehicleLink,
)
from app.schemas.calc import CalcProgramCreate, CalcProgramOut, CalcProgramUpdate, CalcVehicleOut
from app.schemas.catalog import VehicleCatalogCreate, VehicleCatalogOut, VehicleCatalogUpdate, VehicleImageOut
from app.schemas.imports import ImportBatchOut, ImportRunResponse
from app.schemas.leads import LeadOut, LeadUpdate
from app.schemas.offers import OfferOut
from app.schemas.partner import (
    PartnerCreate,
    PartnerOut,
    PartnerRoutingRuleCreate,
    PartnerRoutingRuleOut,
    PartnerRoutingRuleUpdate,
    PartnerUpdate,
)
from app.services.storage import upload_file
from app.workers.tasks import process_import_task

router = APIRouter(prefix="/backoffice", tags=["backoffice"])


@router.post("/partners", response_model=PartnerOut, dependencies=[Depends(require_role("ADMIN"))])
def create_partner(payload: PartnerCreate, db: Session = Depends(get_db)) -> PartnerOut:
    partner = Partner(**payload.model_dump())
    db.add(partner)
    db.commit()
    db.refresh(partner)
    return PartnerOut.model_validate(partner)


@router.get("/partners", response_model=list[PartnerOut], dependencies=[Depends(require_role("ADMIN"))])
def list_partners(db: Session = Depends(get_db)) -> list[PartnerOut]:
    return [PartnerOut.model_validate(p) for p in db.query(Partner).all()]


@router.patch("/partners/{partner_id}", response_model=PartnerOut, dependencies=[Depends(require_role("ADMIN"))])
def update_partner(partner_id: UUID, payload: PartnerUpdate, db: Session = Depends(get_db)) -> PartnerOut:
    partner = db.get(Partner, partner_id)
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(partner, key, value)
    db.commit()
    db.refresh(partner)
    return PartnerOut.model_validate(partner)


@router.delete("/partners/{partner_id}", status_code=204, dependencies=[Depends(require_role("ADMIN"))])
def delete_partner(partner_id: UUID, db: Session = Depends(get_db)) -> None:
    partner = db.get(Partner, partner_id)
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    db.delete(partner)
    db.commit()


@router.post("/partner-routing-rules", response_model=PartnerRoutingRuleOut, dependencies=[Depends(require_role("ADMIN"))])
def create_routing_rule(payload: PartnerRoutingRuleCreate, db: Session = Depends(get_db)) -> PartnerRoutingRuleOut:
    rule = PartnerRoutingRule(**payload.model_dump())
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return PartnerRoutingRuleOut.model_validate(rule)


@router.get("/partner-routing-rules", response_model=list[PartnerRoutingRuleOut], dependencies=[Depends(require_role("ADMIN"))])
def list_routing_rules(db: Session = Depends(get_db)) -> list[PartnerRoutingRuleOut]:
    return [PartnerRoutingRuleOut.model_validate(r) for r in db.query(PartnerRoutingRule).all()]


@router.patch("/partner-routing-rules/{rule_id}", response_model=PartnerRoutingRuleOut, dependencies=[Depends(require_role("ADMIN"))])
def update_routing_rule(rule_id: UUID, payload: PartnerRoutingRuleUpdate, db: Session = Depends(get_db)) -> PartnerRoutingRuleOut:
    rule = db.get(PartnerRoutingRule, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(rule, key, value)
    db.commit()
    db.refresh(rule)
    return PartnerRoutingRuleOut.model_validate(rule)


@router.delete("/partner-routing-rules/{rule_id}", status_code=204, dependencies=[Depends(require_role("ADMIN"))])
def delete_routing_rule(rule_id: UUID, db: Session = Depends(get_db)) -> None:
    rule = db.get(PartnerRoutingRule, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    db.delete(rule)
    db.commit()


@router.post("/imports/upload", response_model=ImportBatchOut, dependencies=[Depends(require_role("ADMIN"))])
def upload_import(
    partner_id: UUID = Form(...),
    adapter_type: str = Form(...),
    program_code: str | None = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> ImportBatchOut:
    file_bytes = file.file.read()
    file_hash = hashlib.sha256(file_bytes).hexdigest()
    existing = db.query(ImportBatch).filter(
        ImportBatch.partner_id == partner_id,
        ImportBatch.source_file_hash == file_hash,
    ).first()
    if existing:
        return ImportBatchOut.model_validate(existing)
    batch = ImportBatch(
        partner_id=partner_id,
        source_filename=file.filename,
        source_file_hash=file_hash,
        uploaded_by_user_id=current_user.id,
        status="uploaded",
        errors_json={"adapter_type": adapter_type, "program_code": program_code},
    )
    db.add(batch)
    db.commit()
    db.refresh(batch)
    os.makedirs("/tmp/imports", exist_ok=True)
    file_path = f"/tmp/imports/{batch.id}_{file.filename}"
    with open(file_path, "wb") as outfile:
        outfile.write(file_bytes)
    batch.errors_json["file_path"] = file_path
    db.commit()
    return ImportBatchOut.model_validate(batch)


@router.post("/imports/{batch_id}/run", response_model=ImportRunResponse, dependencies=[Depends(require_role("ADMIN"))])
def run_import(batch_id: UUID, db: Session = Depends(get_db)) -> ImportRunResponse:
    batch = db.get(ImportBatch, batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Import batch not found")
    metadata = batch.errors_json or {}
    file_path = metadata.get("file_path")
    adapter_type = metadata.get("adapter_type")
    program_code = metadata.get("program_code")
    if not file_path or not adapter_type:
        raise HTTPException(status_code=400, detail="Missing adapter configuration")
    result = process_import_task.delay(str(batch.id), file_path, adapter_type, program_code)
    return ImportRunResponse(task_id=result.id)


@router.get("/imports/{batch_id}", response_model=ImportBatchOut, dependencies=[Depends(require_role("ADMIN"))])
def get_import(batch_id: UUID, db: Session = Depends(get_db)) -> ImportBatchOut:
    batch = db.get(ImportBatch, batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Import batch not found")
    return ImportBatchOut.model_validate(batch)


@router.post("/calc-programs", response_model=CalcProgramOut, dependencies=[Depends(require_role("ADMIN"))])
def create_calc_program(payload: CalcProgramCreate, db: Session = Depends(get_db)) -> CalcProgramOut:
    program = CalcProgram(**payload.model_dump())
    db.add(program)
    db.commit()
    db.refresh(program)
    return CalcProgramOut.model_validate(program)


@router.get("/calc-programs", response_model=list[CalcProgramOut], dependencies=[Depends(require_role("ADMIN"))])
def list_calc_programs(db: Session = Depends(get_db)) -> list[CalcProgramOut]:
    return [CalcProgramOut.model_validate(p) for p in db.query(CalcProgram).all()]


@router.patch("/calc-programs/{program_id}", response_model=CalcProgramOut, dependencies=[Depends(require_role("ADMIN"))])
def update_calc_program(program_id: UUID, payload: CalcProgramUpdate, db: Session = Depends(get_db)) -> CalcProgramOut:
    program = db.get(CalcProgram, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(program, key, value)
    db.commit()
    db.refresh(program)
    return CalcProgramOut.model_validate(program)


@router.delete("/calc-programs/{program_id}", status_code=204, dependencies=[Depends(require_role("ADMIN"))])
def delete_calc_program(program_id: UUID, db: Session = Depends(get_db)) -> None:
    program = db.get(CalcProgram, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    db.delete(program)
    db.commit()


@router.get("/calc-vehicles", response_model=list[CalcVehicleOut], dependencies=[Depends(require_role("ADMIN", "USER"))])
def list_calc_vehicles(db: Session = Depends(get_db)) -> list[CalcVehicleOut]:
    return [CalcVehicleOut.model_validate(v) for v in db.query(CalcVehicle).all()]


@router.post("/vehicles-catalog", response_model=VehicleCatalogOut, dependencies=[Depends(require_role("ADMIN", "USER"))])
def create_vehicle_catalog(
    payload: VehicleCatalogCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> VehicleCatalogOut:
    vehicle = VehicleCatalog(**payload.model_dump(), created_by_user_id=current_user.id)
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return VehicleCatalogOut.model_validate(vehicle)


@router.get("/vehicles-catalog", response_model=list[VehicleCatalogOut], dependencies=[Depends(require_role("ADMIN", "USER"))])
def list_vehicle_catalog(db: Session = Depends(get_db)) -> list[VehicleCatalogOut]:
    vehicles = db.query(VehicleCatalog).options(joinedload(VehicleCatalog.images)).all()
    return [VehicleCatalogOut.model_validate(v) for v in vehicles]


@router.get("/vehicles-catalog/{vehicle_id}", response_model=VehicleCatalogOut, dependencies=[Depends(require_role("ADMIN", "USER"))])
def get_vehicle_catalog(vehicle_id: UUID, db: Session = Depends(get_db)) -> VehicleCatalogOut:
    vehicle = (
        db.query(VehicleCatalog)
        .options(joinedload(VehicleCatalog.images))
        .filter(VehicleCatalog.id == vehicle_id)
        .first()
    )
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return VehicleCatalogOut.model_validate(vehicle)


@router.patch("/vehicles-catalog/{vehicle_id}", response_model=VehicleCatalogOut, dependencies=[Depends(require_role("ADMIN", "USER"))])
def update_vehicle_catalog(vehicle_id: UUID, payload: VehicleCatalogUpdate, db: Session = Depends(get_db)) -> VehicleCatalogOut:
    vehicle = db.get(VehicleCatalog, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(vehicle, key, value)
    vehicle.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(vehicle)
    return VehicleCatalogOut.model_validate(vehicle)


@router.delete("/vehicles-catalog/{vehicle_id}", status_code=204, dependencies=[Depends(require_role("ADMIN", "USER"))])
def delete_vehicle_catalog(vehicle_id: UUID, db: Session = Depends(get_db)) -> None:
    vehicle = db.get(VehicleCatalog, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    db.delete(vehicle)
    db.commit()


@router.post("/vehicles-catalog/{vehicle_id}/images", response_model=VehicleImageOut, dependencies=[Depends(require_role("ADMIN", "USER"))])
def upload_vehicle_image(
    vehicle_id: UUID,
    file: UploadFile = File(...),
    is_cover: bool = Form(False),
    sort_order: int = Form(0),
    alt: str | None = Form(None),
    db: Session = Depends(get_db),
) -> VehicleImageOut:
    vehicle = db.get(VehicleCatalog, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    storage_key = f"vehicles/{vehicle_id}/{file.filename}"
    public_url = upload_file(file.file, storage_key)
    image = VehicleImage(
        vehicle_catalog_id=vehicle_id,
        storage_key=storage_key,
        public_url=public_url,
        sort_order=sort_order,
        alt=alt,
        is_cover=is_cover,
    )
    db.add(image)
    db.commit()
    db.refresh(image)
    return VehicleImageOut.model_validate(image)


@router.post("/vehicles-catalog/{vehicle_id}/link/{calc_vehicle_id}", response_model=dict, dependencies=[Depends(require_role("ADMIN", "USER"))])
def link_vehicle(vehicle_id: UUID, calc_vehicle_id: UUID, db: Session = Depends(get_db)) -> dict:
    vehicle = db.get(VehicleCatalog, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    link = VehicleLink(vehicle_catalog_id=vehicle_id, calc_vehicle_id=calc_vehicle_id)
    db.add(link)
    db.commit()
    db.refresh(link)
    return {"link_id": str(link.id)}


@router.get("/offers", response_model=list[OfferOut], dependencies=[Depends(require_role("ADMIN", "USER"))])
def list_offers(db: Session = Depends(get_db)) -> list[OfferOut]:
    offers = db.query(Offer).options(joinedload(Offer.components)).all()
    return [OfferOut.model_validate(o) for o in offers]


@router.get("/leads", response_model=list[LeadOut], dependencies=[Depends(require_role("ADMIN", "USER"))])
def list_leads(
    partner: UUID | None = None,
    status_filter: str | None = None,
    db: Session = Depends(get_db),
) -> list[LeadOut]:
    query = db.query(Lead)
    if partner:
        query = query.filter(Lead.partner_id == partner)
    if status_filter:
        query = query.filter(Lead.status == status_filter)
    return [LeadOut.model_validate(l) for l in query.all()]


@router.patch("/leads/{lead_id}", response_model=LeadOut, dependencies=[Depends(require_role("ADMIN"))])
def update_lead(lead_id: UUID, payload: LeadUpdate, db: Session = Depends(get_db)) -> LeadOut:
    lead = db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(lead, key, value)
    db.commit()
    db.refresh(lead)
    return LeadOut.model_validate(lead)


@router.post("/leads/{lead_id}/route", response_model=dict, dependencies=[Depends(require_role("ADMIN"))])
def route_lead(lead_id: UUID, db: Session = Depends(get_db)) -> dict:
    lead = db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    lead.status = "contacted"
    lead.routed_at = datetime.utcnow()
    lead.routing_result_json = {"status": "stubbed"}
    db.commit()
    return {"status": "queued"}
