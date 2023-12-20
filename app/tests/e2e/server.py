def test_health_check(client):
    response = client.get("api/ping/")
    assert response.status_code == 200
    assert response.text == '{"code":200,"message":"pong"}'
