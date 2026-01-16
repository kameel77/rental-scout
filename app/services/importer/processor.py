from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.models import (
    CalcCostComponent,
    CalcLine,
    CalcProgram,
    CalcVehicle,
    ImportBatch,
    ImportRow,
    Offer,
    OfferComponent,
    Partner,
)
from app.services.importer.adapters import parse_file


def _upsert_calc_vehicle(db: Session, partner_id, payload: dict[str, Any]) -> CalcVehicle:
    stmt = select(CalcVehicle).where(
        and_(
            CalcVehicle.partner_id == partner_id,
            CalcVehicle.make == payload.get("make"),
            CalcVehicle.model == payload.get("model"),
            CalcVehicle.trim == payload.get("trim"),
            CalcVehicle.external_model_key == payload.get("external_model_key"),
        )
    )
    existing = db.execute(stmt).scalar_one_or_none()
    if existing:
        return existing
    vehicle = CalcVehicle(
        partner_id=partner_id,
        make=payload.get("make"),
        model=payload.get("model"),
        trim=payload.get("trim"),
        full_name=payload.get("full_name"),
        external_model_key=payload.get("external_model_key"),
        meta=payload.get("meta") or {},
    )
    db.add(vehicle)
    db.flush()
    return vehicle


def _upsert_calc_program(db: Session, partner_id, program: dict[str, Any]) -> CalcProgram:
    stmt = select(CalcProgram).where(
        and_(CalcProgram.partner_id == partner_id, CalcProgram.code == program.get("code"))
    )
    existing = db.execute(stmt).scalar_one_or_none()
    if existing:
        return existing
    record = CalcProgram(
        partner_id=partner_id,
        code=program.get("code"),
        name=program.get("code"),
        currency=program.get("currency") or "PLN",
    )
    db.add(record)
    db.flush()
    return record


def _upsert_calc_line(
    db: Session,
    partner_id,
    program_id,
    batch_id,
    vehicle_id,
    normalized: dict[str, Any],
) -> CalcLine:
    scenario = normalized.get("scenario", {})
    stmt = select(CalcLine).where(
        and_(
            CalcLine.calc_program_id == program_id,
            CalcLine.calc_vehicle_id == vehicle_id,
            CalcLine.term_months == scenario.get("term_months"),
            CalcLine.total_mileage_km == scenario.get("total_mileage_km"),
        )
    )
    existing = db.execute(stmt).scalar_one_or_none()
    if existing:
        return existing
    inputs = normalized.get("inputs", {})
    rv = normalized.get("rv", {})
    rm = normalized.get("rm", {})
    book_values = normalized.get("book_values", {})
    record = CalcLine(
        partner_id=partner_id,
        calc_program_id=program_id,
        import_batch_id=batch_id,
        calc_vehicle_id=vehicle_id,
        term_months=scenario.get("term_months"),
        annual_mileage_km=scenario.get("annual_mileage_km"),
        total_mileage_km=scenario.get("total_mileage_km"),
        list_price_gross=inputs.get("list_price_gross"),
        discounted_price_gross=inputs.get("discounted_price_gross"),
        discount_pct=inputs.get("discount_pct"),
        registration_fee_gross=inputs.get("registration_fee_gross"),
        rv_table=rv.get("rv_table"),
        rv_id=rv.get("rv_id"),
        rv_base_pct=rv.get("rv_base_pct"),
        rv_adj_pct=rv.get("rv_adj_pct"),
        rv_pct=rv.get("rv_pct"),
        rv_amount=rv.get("rv_amount"),
        rm_table=rm.get("rm_table"),
        rm_id=rm.get("rm_id"),
        rm_val=rm.get("rm_val"),
        rm_val_per_km=rm.get("rm_val_per_km"),
        rm_amount=rm.get("rm_amount"),
        amortization_amount=normalized.get("amortization_amount"),
        book_value_y1=book_values.get("y1"),
        book_value_y2=book_values.get("y2"),
        book_value_y3=book_values.get("y3"),
        book_value_y4=book_values.get("y4"),
        raw_row=normalized,
    )
    db.add(record)
    db.flush()
    return record


def process_import_batch(
    db: Session,
    batch_id,
    file_path: str,
    adapter_type: str,
    program_code: str | None = None,
) -> dict[str, Any]:
    batch = db.get(ImportBatch, batch_id)
    if not batch:
        raise ValueError("Import batch not found")
    partner = db.get(Partner, batch.partner_id)
    if not partner:
        raise ValueError("Partner not found")
    batch.status = "parsing"
    db.commit()

    normalized_rows = parse_file(file_path, adapter_type, partner.code, program_code=program_code)

    success = 0
    failed = 0
    for idx, normalized in enumerate(normalized_rows, start=1):
        row = ImportRow(
            import_batch_id=batch.id,
            row_number=idx,
            raw_row=normalized,
            normalized_row=normalized,
            status="ok",
        )
        db.add(row)
        try:
            if normalized.get("type") == "OFFERS":
                vehicle = _upsert_calc_vehicle(db, partner.id, normalized.get("calc_vehicle", {}))
                offer_payload = normalized.get("offer", {})
                dedupe_stmt = select(Offer).where(
                    and_(
                        Offer.partner_id == partner.id,
                        Offer.external_offer_id == offer_payload.get("external_offer_id"),
                        Offer.calc_vehicle_id == vehicle.id,
                        Offer.term_months == offer_payload.get("term_months"),
                        Offer.annual_mileage_km == offer_payload.get("annual_mileage_km"),
                        Offer.monthly_total_net == offer_payload.get("monthly_total_net"),
                    )
                )
                existing = db.execute(dedupe_stmt).scalar_one_or_none()
                if not existing:
                    offer = Offer(
                        partner_id=partner.id,
                        import_batch_id=batch.id,
                        calc_vehicle_id=vehicle.id,
                        external_offer_id=offer_payload.get("external_offer_id"),
                        term_months=offer_payload.get("term_months"),
                        annual_mileage_km=offer_payload.get("annual_mileage_km"),
                        total_mileage_km=offer_payload.get("total_mileage_km"),
                        currency=offer_payload.get("currency") or partner.default_currency,
                        vat_rate=offer_payload.get("vat_rate"),
                        upfront_fee_net=offer_payload.get("upfront_fee_net"),
                        monthly_total_net=offer_payload.get("monthly_total_net"),
                        notes=offer_payload.get("notes"),
                        raw_row=normalized,
                    )
                    db.add(offer)
                    db.flush()
                    for component in normalized.get("components", []):
                        db.add(
                            OfferComponent(
                                offer_id=offer.id,
                                component_code=component.get("component_code"),
                                label=component.get("label"),
                                amount_net=component.get("amount_net"),
                                amount_gross=component.get("amount_gross"),
                                unit=component.get("unit"),
                                included=component.get("included", True),
                                meta=component.get("meta") or {},
                            )
                        )
            if normalized.get("type") == "CALC_RATECARD":
                vehicle = _upsert_calc_vehicle(db, partner.id, normalized.get("calc_vehicle", {}))
                program = _upsert_calc_program(db, partner.id, normalized.get("program", {}))
                line = _upsert_calc_line(db, partner.id, program.id, batch.id, vehicle.id, normalized)
                for component in normalized.get("cost_components", []):
                    db.add(
                        CalcCostComponent(
                            calc_line_id=line.id,
                            component_code=component.get("component_code"),
                            label=component.get("label"),
                            amount=component.get("amount"),
                            unit=component.get("unit"),
                            meta=component.get("meta") or {},
                        )
                    )
            success += 1
        except Exception as exc:
            row.status = "failed"
            row.error_message = str(exc)
            failed += 1
        db.flush()

    batch.status = "parsed" if failed == 0 else "failed"
    batch.rows_total = len(normalized_rows)
    batch.rows_success = success
    batch.rows_failed = failed
    batch.parsed_at = datetime.utcnow()
    db.commit()
    return {"success": success, "failed": failed}
