from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, select
from sqlalchemy.orm import Session, joinedload

from app.db import get_db
from app.models import Offer, OfferComponent, VehicleCatalog, VehicleLink
from app.schemas.catalog import VehicleCatalogOut
from app.schemas.leads import LeadCreate, LeadOut
from app.schemas.offers import OfferOut
from app.models import Lead

router = APIRouter(prefix="/public", tags=["public"])


@router.get("/vehicles", response_model=list[VehicleCatalogOut])
def list_public_vehicles(
    make: str | None = None,
    model: str | None = None,
    db: Session = Depends(get_db),
) -> list[VehicleCatalogOut]:
    query = db.query(VehicleCatalog).options(joinedload(VehicleCatalog.images))
    query = query.filter(VehicleCatalog.is_published.is_(True))
    if make:
        query = query.filter(VehicleCatalog.make.ilike(f"%{make}%"))
    if model:
        query = query.filter(VehicleCatalog.model.ilike(f"%{model}%"))
    return [VehicleCatalogOut.model_validate(row) for row in query.all()]


@router.get("/vehicles/{vehicle_id}", response_model=VehicleCatalogOut)
def get_public_vehicle(vehicle_id: str, db: Session = Depends(get_db)) -> VehicleCatalogOut:
    vehicle = (
        db.query(VehicleCatalog)
        .options(joinedload(VehicleCatalog.images))
        .filter(VehicleCatalog.id == vehicle_id, VehicleCatalog.is_published.is_(True))
        .first()
    )
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return VehicleCatalogOut.model_validate(vehicle)


@router.get("/vehicles/{vehicle_id}/offers", response_model=list[OfferOut])
def get_vehicle_offers(
    vehicle_id: str,
    term: int | None = None,
    mileage: int | None = None,
    partner: str | None = None,
    db: Session = Depends(get_db),
) -> list[OfferOut]:
    link = db.query(VehicleLink).filter(VehicleLink.vehicle_catalog_id == vehicle_id).first()
    if not link:
        return []
    query = db.query(Offer).options(joinedload(Offer.components))
    query = query.filter(Offer.calc_vehicle_id == link.calc_vehicle_id)
    if term:
        query = query.filter(Offer.term_months == term)
    if mileage:
        query = query.filter(Offer.annual_mileage_km == mileage)
    if partner:
        query = query.filter(Offer.partner_id == partner)
    return [OfferOut.model_validate(row) for row in query.all()]


@router.get("/offers", response_model=list[OfferOut])
def search_offers(
    make: str | None = None,
    model: str | None = None,
    term: int | None = None,
    mileage: int | None = None,
    price_min: float | None = None,
    price_max: float | None = None,
    partner: str | None = None,
    db: Session = Depends(get_db),
) -> list[OfferOut]:
    query = db.query(Offer).options(joinedload(Offer.components))
    if term:
        query = query.filter(Offer.term_months == term)
    if mileage:
        query = query.filter(Offer.annual_mileage_km == mileage)
    if partner:
        query = query.filter(Offer.partner_id == partner)
    if price_min is not None:
        query = query.filter(Offer.monthly_total_net >= price_min)
    if price_max is not None:
        query = query.filter(Offer.monthly_total_net <= price_max)
    if make or model:
        query = query.filter(Offer.calc_vehicle_id.is_not(None))
        subquery = select(VehicleLink.calc_vehicle_id).join(
            VehicleCatalog, VehicleLink.vehicle_catalog_id == VehicleCatalog.id
        )
        filters = []
        if make:
            filters.append(VehicleCatalog.make.ilike(f"%{make}%"))
        if model:
            filters.append(VehicleCatalog.model.ilike(f"%{model}%"))
        if filters:
            subquery = subquery.filter(and_(*filters))
        query = query.filter(Offer.calc_vehicle_id.in_(subquery))
    return [OfferOut.model_validate(row) for row in query.all()]


@router.get("/offers/{offer_id}")
def get_offer(offer_id: str, db: Session = Depends(get_db)) -> dict:
    offer = db.query(Offer).options(joinedload(Offer.components)).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    vehicle_catalog = (
        db.query(VehicleCatalog)
        .join(VehicleLink, VehicleLink.vehicle_catalog_id == VehicleCatalog.id)
        .filter(VehicleLink.calc_vehicle_id == offer.calc_vehicle_id)
        .first()
    )
    return {
        "offer": OfferOut.model_validate(offer),
        "vehicle_catalog": VehicleCatalogOut.model_validate(vehicle_catalog) if vehicle_catalog else None,
    }


@router.post("/leads", response_model=LeadOut)
def create_lead(payload: LeadCreate, db: Session = Depends(get_db)) -> LeadOut:
    offer = db.query(Offer).filter(Offer.id == payload.offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    lead = Lead(
        partner_id=offer.partner_id,
        offer_id=offer.id,
        status="new",
        contact_json=payload.contact_json,
        notes=payload.notes,
        source=payload.source,
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return LeadOut.model_validate(lead)
