import os

import pytest

from adz.cfg import CFG

PARAMETERS = [
    # test default value
    [
        {"path": None, "settings": {}, "variables": {}, "endpoints": {}},
        {
            "path": None,
            "settings": {"colors": True, "response": True, "theme": "native"},
            "variables": {},
            "endpoints": {},
        },
    ],
    [
        {
            "path": None,
            "settings": {},
            "variables": {"abc": "CBA"},
            "endpoints": {"n": {"headers": {"a": "B"}}},
        },
        {
            "path": None,
            "settings": {"colors": True, "response": True, "theme": "native"},
            "variables": {"abc": "CBA"},
            "endpoints": {"n": {"headers": {"a": "B"}}},
        },
    ],
    [
        {
            "path": None,
            "settings": {},
            "variables": {"abc": "CBA"},
            "endpoints": {"n": {"headers": [{"a": "B"}]}},
        },
        {
            "path": None,
            "settings": {"colors": True, "response": True, "theme": "native"},
            "variables": {"abc": "CBA"},
            "endpoints": {"n": {"headers": {"a": "B"}}},
        },
    ],
    # method uppercase
    [
        {
            "path": None,
            "settings": {},
            "variables": {},
            "endpoints": {"n": {"method": "get"}},
        },
        {
            "path": None,
            "settings": {"colors": True, "response": True, "theme": "native"},
            "variables": {},
            "endpoints": {"n": {"headers": {}, "method": "GET"}},
        },
    ],
    # test request conversion to method and url
    [
        {
            "path": None,
            "settings": {},
            "variables": {},
            "endpoints": {"n": {"request": "get http://url.com"}},
        },
        {
            "path": None,
            "settings": {"colors": True, "response": True, "theme": "native"},
            "variables": {},
            "endpoints": {
                "n": {"headers": {}, "method": "GET", "url": "http://url.com"}
            },
        },
    ],
    # test variables interpolation
    [
        {
            "path": None,
            "settings": {},
            "variables": {"abc": "CBA"},
            "endpoints": {"n": {"headers": {"a": "B $abc"}}},
        },
        {
            "path": None,
            "settings": {"colors": True, "response": True, "theme": "native"},
            "variables": {"abc": "CBA"},
            "endpoints": {"n": {"headers": {"a": "B CBA"}}},
        },
    ],
    [
        {
            "path": None,
            "settings": {},
            "variables": {"abc": "CBA"},
            "endpoints": {"n": {"url": "http://$abc.com/$abc"}},
        },
        {
            "path": None,
            "settings": {"colors": True, "response": True, "theme": "native"},
            "variables": {"abc": "CBA"},
            "endpoints": {"n": {"headers": {}, "url": "http://CBA.com/CBA"}},
        },
    ],
    # test files
    [
        {
            "path": None,
            "settings": {},
            "variables": {"abc": "CBA"},
            "endpoints": {"n": {"files": {"a": "a.txt"}}},
        },
        {
            "path": None,
            "settings": {"colors": True, "response": True, "theme": "native"},
            "variables": {"abc": "CBA"},
            "endpoints": {"n": {"headers": {}, "files": {"a": "a.txt"}}},
        },
    ],
    [
        {
            "path": None,
            "settings": {},
            "variables": {"abc": "CBA"},
            "endpoints": {"n": {"files": ["a.txt"]}},
        },
        {
            "path": None,
            "settings": {"colors": True, "response": True, "theme": "native"},
            "variables": {"abc": "CBA"},
            "endpoints": {"n": {"headers": {}, "files": {"a.txt": "a.txt"}}},
        },
    ],
    [
        {
            "path": None,
            "settings": {},
            "variables": {"abc": "CBA"},
            "endpoints": {"n": {"files": "a.txt"}},
        },
        {
            "path": None,
            "settings": {"colors": True, "response": True, "theme": "native"},
            "variables": {"abc": "CBA"},
            "endpoints": {"n": {"headers": {}, "files": {"a.txt": "a.txt"}}},
        },
    ],
    # test json / data
    [
        {
            "path": None,
            "settings": {},
            "variables": {"abc": "CBA"},
            "endpoints": {"n": {"data": {"a": 1, "b": 2}}},
        },
        {
            "path": None,
            "settings": {"colors": True, "response": True, "theme": "native"},
            "variables": {"abc": "CBA"},
            "endpoints": {"n": {"headers": {}, "data": {"a": 1, "b": 2}}},
        },
    ],
    # test json / data file
    [
        {
            "path": None,
            "settings": {},
            "variables": {"abc": "CBA"},
            "endpoints": {"n": {"json": "file://./readme.md"}},
        },
        {
            "path": None,
            "settings": {"colors": True, "response": True, "theme": "native"},
            "variables": {"abc": "CBA"},
            "endpoints": {"n": {"headers": {}, "json": "file://./readme.md"}},
        },
    ],
    # test params / cookies
    [
        {
            "path": None,
            "settings": {"colors": False},
            "variables": {"abc": "CBA"},
            "endpoints": {"n": {"params": [{"a": "A"}, {"b": "B"}]}},
        },
        {
            "path": None,
            "settings": {"colors": False, "response": True, "theme": "native"},
            "variables": {"abc": "CBA"},
            "endpoints": {"n": {"headers": {}, "params": {"a": "A", "b": "B"}}},
        },
    ],
]


@pytest.mark.parametrize("input,output", PARAMETERS)
def test_cfg_init(input: dict, output: dict):
    assert CFG(**input).to_dict() == output, (input, output)


@pytest.mark.parametrize("input,output", PARAMETERS)
def test_cfg_configure(config, input: dict, output: dict):
    path = str(config(input))
    assert CFG.configure(path=path).to_dict() == {**output, "path": path}


def test_cfg_configure_json_file(config, tmpdir):
    file = tmpdir.join("file.json")
    file.write('{"a":1,"b":2}')
    data = {
        "endpoints": {
            "n": {"headers": {}, "json": f"file://{file}", "data": f"file://{file}"}
        }
    }
    path = str(config(data))
    assert CFG.configure(path=path).to_dict() == {
        "path": path,
        "settings": {"colors": True, "response": True, "theme": "native"},
        "variables": {},
        "endpoints": {
            "n": {"headers": {}, "json": {"a": 1, "b": 2}, "data": {"a": 1, "b": 2}}
        },
    }


def test_cfg_configure_env_path(config):
    data = {"endpoints": {"n": {"headers": {}}}}
    path = str(config(data))
    os.environ["ADZ"] = path
    cfg = CFG.configure(path=None)
    assert cfg.to_dict() == {
        "path": path,
        "settings": {"response": True, "theme": "native", "colors": True},
        "variables": {},
        "endpoints": {"n": {"headers": {}}},
    }
    os.environ.pop("ADZ")


def test_cfg_configure_no_path():
    cfg = CFG.configure(path=None)
    assert cfg is None
