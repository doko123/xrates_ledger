def test_last(client, db, cache):
    response = client.get("/last")
    assert 200 == response.status_code
