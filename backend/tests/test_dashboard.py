def test_dashboard_summary(client):
    response = client.get("/api/dashboard/summary")
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload["total_districts"], int)
    assert "high_risk" in payload
    assert "active_alerts" in payload


def test_hotspots_non_empty(client):
    response = client.get("/api/dashboard/hotspots")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
