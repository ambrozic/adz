from adz import ADZ, CFG


def test_call_get(server):
    url = f"{server.address}/endpoint/"
    config = CFG(
        path="",
        settings={},
        variables={},
        endpoints={
            "name": {
                "headers": {"content-type": "application/json"},
                "request": f"get {url}",
                "params": {"a": 1, "b": 2},
                "cookies": {"ca": 1, "cb": 2},
            }
        },
    )
    response = ADZ(config=config)(name="name")
    assert response.method == "GET"
    assert response.url == f"{url}?a=1&b=2"
    assert response.status_code == 200


def test_call_post(server):
    url = f"{server.address}/endpoint/"
    config = CFG(
        path="",
        settings={},
        variables={},
        endpoints={
            "name": {
                "headers": {"content-type": "application/json"},
                "request": f"post {url}",
                "json": {"a": 1},
            }
        },
    )
    response = ADZ(config=config)(name="name")
    assert response.method == "POST"
    assert response.url == url
    assert response.status_code == 200


def test_call_post_files(server, tmpdir):
    file = tmpdir.join("file.json")
    file.write('{"a":1,"b":2}')
    url = f"{server.address}/endpoint/"
    config = CFG(
        path="",
        settings={},
        variables={},
        endpoints={
            "name": {
                "headers": {"content-type": "application/json"},
                "request": f"post {url}",
                "files": [str(file)],
            }
        },
    )
    response = ADZ(config=config)(name="name")
    assert response.method == "POST"
    assert response.url == url
    assert response.status_code == 200


def test_call_no_config(server):
    response = ADZ(config=None)(name="name")
    assert response is None


def test_call_endpoint_does_not_exist(server):
    url = f"{server.address}/endpoint/"
    config = CFG(
        path="",
        settings={},
        variables={},
        endpoints={"name": {"request": f"get {url}"}},
    )
    response = ADZ(config=config)(name="abc")
    assert response is None


def test_response_to_dict(server):
    url = f"{server.address}/endpoint/"
    config = CFG(
        path="",
        settings={},
        variables={},
        endpoints={"name": {"request": f"get {url}"}},
    )
    response = ADZ(config=config)(name="name")
    assert list(response.__slots__).sort() == list(response.to_dict().keys()).sort()
