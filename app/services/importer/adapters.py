from __future__ import annotations

from typing import Any

import pandas as pd


def _standardize_columns(frame: pd.DataFrame) -> pd.DataFrame:
    frame.columns = [str(col).strip() for col in frame.columns]
    return frame


def parse_basket_like(frame: pd.DataFrame, partner_code: str) -> list[dict[str, Any]]:
    frame = _standardize_columns(frame)
    normalized: list[dict[str, Any]] = []
    for _, row in frame.iterrows():
        normalized.append(
            {
                "type": "OFFERS",
                "partner_code": partner_code,
                "calc_vehicle": {
                    "make": row.get("marka") or row.get("Marka"),
                    "model": row.get("model") or row.get("Model"),
                    "trim": row.get("wersja") or row.get("Wersja"),
                    "full_name": row.get("nazwa") or row.get("Nazwa"),
                    "external_model_key": None,
                    "meta": {},
                },
                "offer": {
                    "external_offer_id": None,
                    "term_months": int(row.get("okres") or row.get("Okres")),
                    "annual_mileage_km": int(row.get("przebieg") or row.get("Przebieg")),
                    "total_mileage_km": int(row.get("przebieg") or row.get("Przebieg"))
                    * int(row.get("okres") or row.get("Okres"))
                    // 12,
                    "currency": "PLN",
                    "vat_rate": None,
                    "upfront_fee_net": None,
                    "monthly_total_net": float(row.get("rate") or row.get("Rate")),
                    "notes": None,
                },
                "components": [],
            }
        )
    return normalized


def parse_ayvens_like(frame: pd.DataFrame, partner_code: str) -> list[dict[str, Any]]:
    frame = _standardize_columns(frame)
    normalized: list[dict[str, Any]] = []
    for _, row in frame.iterrows():
        normalized.append(
            {
                "type": "OFFERS",
                "partner_code": partner_code,
                "calc_vehicle": {
                    "make": row.get("Make"),
                    "model": row.get("Model"),
                    "trim": row.get("Trim"),
                    "full_name": row.get("Full Name") or row.get("Model"),
                    "external_model_key": row.get("External Model Key"),
                    "meta": {"spec_number": row.get("Spec Number")},
                },
                "offer": {
                    "external_offer_id": row.get("Offer ID"),
                    "term_months": int(row.get("Term")),
                    "annual_mileage_km": int(row.get("Annual Mileage")),
                    "total_mileage_km": int(row.get("Total Mileage") or 0),
                    "currency": row.get("Currency") or "PLN",
                    "vat_rate": float(row.get("VAT")) if row.get("VAT") else None,
                    "upfront_fee_net": float(row.get("Upfront Net")) if row.get("Upfront Net") else None,
                    "monthly_total_net": float(row.get("Monthly Net")) if row.get("Monthly Net") else None,
                    "notes": row.get("Notes"),
                },
                "components": [],
            }
        )
    return normalized


def parse_athlon_like(frame: pd.DataFrame, partner_code: str) -> list[dict[str, Any]]:
    frame = _standardize_columns(frame)
    normalized: list[dict[str, Any]] = []
    component_columns = [
        col
        for col in frame.columns
        if col not in {"Make", "Model", "Trim", "Term", "Annual Mileage", "Monthly Net"}
    ]
    for _, row in frame.iterrows():
        components: list[dict[str, Any]] = []
        for col in component_columns:
            value = row.get(col)
            if pd.isna(value):
                continue
            components.append(
                {
                    "component_code": col.upper().replace(" ", "_"),
                    "label": col,
                    "amount_net": float(value),
                    "unit": "MONTHLY",
                    "included": True,
                    "meta": {},
                }
            )
        normalized.append(
            {
                "type": "OFFERS",
                "partner_code": partner_code,
                "calc_vehicle": {
                    "make": row.get("Make"),
                    "model": row.get("Model"),
                    "trim": row.get("Trim"),
                    "full_name": row.get("Model"),
                    "external_model_key": None,
                    "meta": {},
                },
                "offer": {
                    "external_offer_id": None,
                    "term_months": int(row.get("Term")),
                    "annual_mileage_km": int(row.get("Annual Mileage")),
                    "total_mileage_km": int(row.get("Annual Mileage")) * int(row.get("Term")) // 12,
                    "currency": "PLN",
                    "vat_rate": None,
                    "upfront_fee_net": None,
                    "monthly_total_net": float(row.get("Monthly Net")),
                    "notes": None,
                },
                "components": components,
            }
        )
    return normalized


def parse_calc_ratecard(frame: pd.DataFrame, partner_code: str, program_code: str) -> list[dict[str, Any]]:
    frame = _standardize_columns(frame)
    normalized: list[dict[str, Any]] = []
    for _, row in frame.iterrows():
        components: list[dict[str, Any]] = []
        for col in frame.columns:
            if str(col).startswith("Unnamed"):
                value = row.get(col)
                if pd.isna(value):
                    continue
                components.append(
                    {
                        "component_code": f"UNKNOWN_{col.split(':')[-1].strip()}",
                        "label": col,
                        "amount": float(value),
                        "unit": "OTHER",
                        "meta": {},
                    }
                )
        normalized.append(
            {
                "type": "CALC_RATECARD",
                "partner_code": partner_code,
                "program": {"code": program_code, "currency": "PLN"},
                "calc_vehicle": {
                    "make": row.get("Marka"),
                    "model": row.get("Model / Wersja"),
                    "trim": row.get("Model / Wersja"),
                    "full_name": row.get("Model / Wersja"),
                },
                "scenario": {
                    "term_months": int(row.get("Okres")),
                    "annual_mileage_km": int(row.get("Przebieg Roczny")),
                    "total_mileage_km": int(row.get("Przebieg")),
                },
                "inputs": {
                    "list_price_gross": row.get("Cena katalogowa PLN brutto"),
                    "discounted_price_gross": row.get("Cena po upuście PLN brutto"),
                    "discount_pct": row.get("Rabat"),
                    "registration_fee_gross": row.get("Rejestracja"),
                },
                "rv": {
                    "rv_table": row.get("RV_Table"),
                    "rv_id": row.get("RV_ID"),
                    "rv_base_pct": row.get("RV_Base"),
                    "rv_adj_pct": row.get("RV_Adj"),
                    "rv_pct": row.get("RV %"),
                    "rv_amount": row.get("RV"),
                },
                "rm": {
                    "rm_table": row.get("RM Table"),
                    "rm_id": row.get("RM_ID"),
                    "rm_val": row.get("RM_Val"),
                    "rm_val_per_km": row.get("RM_Val_per km"),
                    "rm_amount": row.get("RM"),
                },
                "book_values": {
                    "y1": row.get("Bookvalue Y1"),
                    "y2": row.get("Bookvalue Y2"),
                    "y3": row.get("Bookvalue Y3"),
                    "y4": row.get("Bookvalue Y4"),
                },
                "amortization_amount": row.get("Amortyzacja"),
                "cost_components": components,
            }
        )
    return normalized


def parse_file(path: str, adapter_type: str, partner_code: str, program_code: str | None = None) -> list[dict[str, Any]]:
    if path.lower().endswith(".csv"):
        frame = pd.read_csv(path)
    else:
        frame = pd.read_excel(path)

    if adapter_type == "basket-like":
        return parse_basket_like(frame, partner_code)
    if adapter_type == "ayvens-like":
        return parse_ayvens_like(frame, partner_code)
    if adapter_type == "athlon-like":
        return parse_athlon_like(frame, partner_code)
    if adapter_type == "calc-ratecard":
        if not program_code:
            raise ValueError("program_code is required for calc-ratecard")
        return parse_calc_ratecard(frame, partner_code, program_code)
    raise ValueError(f"Unknown adapter type: {adapter_type}")
