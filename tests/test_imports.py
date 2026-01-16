import io

from app.models import Partner


def test_upload_and_enqueue_import(client, db_session, user_token):
    partner = Partner(name="Partner", code="TEST", workflow_key="default")
    db_session.add(partner)
    db_session.commit()

    files = {
        "file": ("sample.csv", b"marka,model,okres,przebieg,rate\nRenault,Austral,36,15000,1899.99\n")
    }
    data = {
        "partner_id": str(partner.id),
        "adapter_type": "basket-like",
        "program_code": "RENTAL_05_2025",
    }
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.post("/backoffice/imports/upload", data=data, files=files, headers=headers)
    assert response.status_code == 200
    batch_id = response.json()["id"]

    run_response = client.post(f"/backoffice/imports/{batch_id}/run", headers=headers)
    assert run_response.status_code == 200
    assert "task_id" in run_response.json()
