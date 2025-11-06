def test_patient_crud(client):
    # create
    r = client.post("/api/patients", json={"name":"Alice","dob":"1990-01-01","email":"a@x.com"})
    assert r.status_code == 201
    pid = r.get_json()["id"]
    # get
    r = client.get(f"/api/patients/{pid}")
    assert r.status_code == 200
    assert r.get_json()["name"] == "Alice"
    # list
    r = client.get("/api/patients")
    assert r.status_code == 200
    assert len(r.get_json()) == 1
    # update
    r = client.patch(f"/api/patients/{pid}", json={"phone":"123"})
    assert r.status_code == 200
    # delete
    r = client.delete(f"/api/patients/{pid}")
    assert r.status_code == 200
    # not found
    r = client.get(f"/api/patients/{pid}")
    assert r.status_code == 404
