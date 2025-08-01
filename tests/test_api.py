import os
import json

# Keep tests deterministic and offline-friendly
os.environ["DRY_RUN"] = "1"

from src.app.server import app  # imports the Flask app without running the server

def test_health():
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}

def test_extract_structured_with_text():
    client = app.test_client()
    payload = {
        "text": "MOCK STORE\nInvoice: INV-001\n2x Widget @ 3.50\nSubtotal: 7.00\nTax: 0.63\nTotal: 7.63\nPaid: VISA ****1111"
    }
    resp = client.post(
        "/extract_structured",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert resp.status_code == 200
    data = resp.get_json()
    # minimal schema checks
    assert "vendor" in data and "items" in data and "payment" in data and "raw_text" in data
    assert data["vendor"]["name"] == "Mock Store"
    assert isinstance(data["items"], list) and len(data["items"]) >= 1
    assert data["payment"]["total"] == 7.63
