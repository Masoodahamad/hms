def test_average_age(client):
    # seed patients
    client.post("/api/patients", json={"name":"A","dob":"1990-01-01"})
    client.post("/api/patients", json={"name":"B","dob":"2000-01-01"})
    r = client.get("/api/analytics/average-age?batch_size=1")
    assert r.status_code == 200
    # number sanity
    assert r.get_json()["average_age"] > 0
