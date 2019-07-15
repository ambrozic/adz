import json

from click.testing import CliRunner

from adz import cli


def test_cli_args(config):
    runner = CliRunner()
    data = {
        "settings": {"colors": False},
        "variables": {"a": 1, "b": 2},
        "endpoints": {"n": {"headers": {"ha": "$a", "hb": "b"}}},
    }

    result = runner.invoke(cli.main, ["-c", "abc"])
    assert 'Path "abc" does not exist.' in result.output

    result = runner.invoke(cli.main, ["-c", None])
    assert "Missing configuration file" in result.output

    result = runner.invoke(cli.main, ["-l", "-c", config(data)])
    assert "  » Endpoints" in result.output

    result = runner.invoke(cli.main, ["-o", "-c", config(data)])
    assert "  » Configuration" in result.output

    result = runner.invoke(cli.main, ["-s", "-c", config(data)])
    assert "  » Settings" in result.output

    result = runner.invoke(cli.main, ["-v", "a=11", "-o", "-c", config(data)])
    assert '  "ha": "11"' in result.output
    assert '  "hb": "b"' in result.output
    assert '  "a": "11"' in result.output
    assert '  "b": 2' in result.output

    result = runner.invoke(cli.main, ["abc", "-c", config(data)])
    assert '"abc" endpoint does not exist' in result.output
    result = runner.invoke(cli.main, ["n", "-d", "-c", config(data)])
    assert '  » Endpoint "n"' in result.output

    result = runner.invoke(cli.main, ["-c", "/path/to/no/cfg.yml"])
    assert 'Error: Invalid value for "--config" / "-c":' in result.output
    assert 'Path "/path/to/no/cfg.yml" does not exist' in result.output


def test_cli_endpoint(server, config):
    runner = CliRunner()
    data = {
        "settings": {"colors": False, "response": True, "theme": "native"},
        "variables": {"abc": "CBA"},
        "endpoints": {
            "n": {
                "request": f"get {server.address}/endpoint/",
                "headers": {},
                "params": {"a": "A", "b": "B"},
            }
        },
    }
    result = runner.invoke(cli.main, ["-c", config(data)])
    assert "  ADZ command line interface" in result.output

    result = runner.invoke(cli.main, ["-c", config(data), "abc"])
    assert '"abc" endpoint does not exist' in result.output

    result = runner.invoke(cli.main, ["-c", config(data), "n"])
    assert f"GET {server.address}/endpoint/?a=A&b=B\n" in result.output
    assert "HTTP/1.1 200 OK\n" in result.output
    assert "server: uvicorn\n" in result.output

    response = json.loads(result.output.split("\n\n")[1])
    assert "headers" in response
    assert response["method"] == "GET"
    assert response["path"] == "/endpoint/"
