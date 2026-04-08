def test_get_alerts(client):
    response = client.get("/api/alerts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_patch_alert_blocked_in_demo_mode(client):
    response = client.patch("/api/alerts/1", json={"status": "resolved"})
    assert response.status_code == 403
