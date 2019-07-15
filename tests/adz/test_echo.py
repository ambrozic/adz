from adz import CFG, Echo


def test_call_no_colors(capsys):
    config = CFG(path="", settings={"colors": False}, variables={}, endpoints={})
    echo = Echo(config=config)

    echo("123")
    captured = capsys.readouterr()
    assert "123\n" == captured.out

    echo({"a": 1})
    captured = capsys.readouterr()
    assert '{\n    "a": 1\n}\n' == captured.out

    echo("")
    captured = capsys.readouterr()
    assert "\n" == captured.out

    echo(b"JSONDecodeError")
    captured = capsys.readouterr()
    assert "JSONDecodeError\n" == captured.out


def test_call_colors(capsys):
    config = CFG(path="", settings={"colors": True}, variables={}, endpoints={})
    echo = Echo(config=config)

    echo("abc")
    captured = capsys.readouterr()
    assert "mabc" in captured.out

    echo([1, 2, 3])
    captured = capsys.readouterr()
    for s in ["    1,", "    2,", "    3"]:
        assert s in captured.out, s
