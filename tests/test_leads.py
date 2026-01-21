from app.models import ImportBatch, Offer, Partner


def test_create_lead(client, db_session):
    partner = Partner(name="Partner", code="TEST", workflow_key="default")
    db_session.add(partner)
    db_session.commit()
    batch = ImportBatch(partner_id=partner.id, source_filename="file.csv", source_file_hash="hash", status="uploaded")
    db_session.add(batch)
    db_session.commit()
    offer = Offer(
        partner_id=partner.id,
        import_batch_id=batch.id,
        term_months=24,
        annual_mileage_km=10000,
        currency="PLN",
    )
    db_session.add(offer)
    db_session.commit()

    response = client.post(
        "/public/leads",
        json={"offer_id": str(offer.id), "contact_json": {"name": "A"}, "source": "web"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "new"
