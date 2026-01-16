from app.models import VehicleCatalog


def test_public_vehicles(client, db_session):
    vehicle = VehicleCatalog(title="Test", make="Ford", model="Focus", is_published=True)
    db_session.add(vehicle)
    db_session.commit()

    response = client.get("/public/vehicles")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["make"] == "Ford"
