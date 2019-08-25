import glob
import json
import os
import typing
from pathlib import Path
from string import Template

import yaml


class CFG:
    def __init__(self, path: str, settings: dict, variables: dict, endpoints: dict):
        self.path = path
        self.settings = {
            **dict(response=True, theme="native", colors=True),
            **(settings or {}),
        }
        self.variables = variables or dict()
        self.endpoints = endpoints or dict()

        for key, value in self.variables.items():
            if isinstance(value, str) and value.startswith("file://"):
                self.variables[key] = self.file_to_string(path=value)

        for name, v in self.endpoints.items():
            for key, value in dict(v).items():
                if key == "request":
                    request = v.pop("request", "").split(maxsplit=1) or ["", ""]
                    for i, n in enumerate(["method", "url"]):
                        self.endpoints[name][n] = v.get(n, request[i])

                if (
                    key in ["json", "data"]
                    and isinstance(value, str)
                    and value.startswith("file://")
                ):
                    try:
                        content = self.file_to_string(path=value)
                        self.endpoints[name][key] = json.loads(content)
                    except json.decoder.JSONDecodeError:
                        pass

                if key in ["files"]:
                    if isinstance(value, list):
                        self.endpoints[name]["files"] = {fn: fn for fn in value}
                    if isinstance(value, str):
                        self.endpoints[name]["files"] = {value: value}

                if key in ["params", "cookies", "headers"] and isinstance(value, list):
                    self.endpoints[name][key] = dict(
                        [tuple(h.items())[0] for h in value]
                    )

            self.endpoints[name]["headers"] = {
                hk: Template(hv).safe_substitute(self.variables)
                for hk, hv in v.get("headers", {}).items()
            }
            if "url" in self.endpoints[name]:
                url = self.endpoints[name]["url"]
                self.endpoints[name]["url"] = Template(url).safe_substitute(
                    self.variables
                )
            if "cookies" in self.endpoints[name]:
                self.endpoints[name]["cookies"] = {
                    k: str(v) for k, v in self.endpoints[name]["cookies"].items()
                }
            if "method" in self.endpoints[name]:
                self.endpoints[name]["method"] = self.endpoints[name]["method"].upper()

    @classmethod
    def configure(
        cls, path: str = None, variables: dict = None, settings: dict = None
    ) -> typing.Optional["CFG"]:
        if not path:
            paths = ["", ".adz/", f"{Path.home()}/.adz/"]
            files = ["adz.y*ml", "api.y*ml", "rest.y*ml"]
            locations = [f"{p}{f}" for p in paths for f in files] + [
                os.environ.get("ADZ", "-")
            ]
            for p in [glob.glob(loc) for loc in locations]:
                if not p:
                    continue
                path = p[0]

        if not path:  # pragma: no cover
            return

        path = os.path.realpath(path)
        with open(path, "r") as f:
            content = yaml.load(f.read(), Loader=yaml.Loader)

        s = content.get("settings") or {}
        content["settings"] = {
            **s,
            **{
                name: s.get(name, True) if value is None else value
                for name, value in (settings or {}).items()
            },
        }

        content["variables"] = {**(content.get("variables") or {}), **(variables or {})}

        return cls(
            path=path,
            **{a: content.get(a) or {} for a in ["settings", "variables", "endpoints"]},
        )

    def file_to_string(self, path):
        path = os.path.realpath(path[7:] if path.startswith("file://") else path)
        with open(path, "r") as f:
            return f.read().strip()

    def to_dict(self) -> dict:
        return dict(
            path=self.path,
            settings=self.settings,
            variables=self.variables,
            endpoints=self.endpoints,
        )
