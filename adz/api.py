import http

import requests

from .cfg import CFG

CODES = {c.value: c.phrase for c in http.HTTPStatus}


class Response:
    __slots__ = (
        "method",
        "url",
        "http_version",
        "status_code",
        "status_phrase",
        "headers",
        "content",
    )

    def __init__(
        self,
        method: str,
        url: str,
        http_version: str,
        status_code: int,
        headers: dict,
        content: bytes,
    ):
        self.method = method
        self.url = url
        self.http_version = http_version
        self.status_code = status_code
        self.status_phrase = CODES[status_code]
        self.headers = headers
        self.content = content

    def to_dict(self):
        return {o: getattr(self, o) for o in self.__slots__}


class ADZ:
    def __init__(self, config: CFG):
        self.config = config

    def __call__(self, name):
        if not self.config or name not in self.config.endpoints:
            return

        endpoint = self.config.endpoints[name]
        url = endpoint.get("url")
        method = endpoint.get("method")
        headers = endpoint.get("headers")
        files = endpoint.get("files", {})

        response = requests.request(
            method=method,
            url=url,
            params=endpoint.get("params"),
            data=endpoint.get("data"),
            files={n: open(p, "rb") for n, p in files.items()} or None,
            json=endpoint.get("json"),
            headers=headers,
            cookies=endpoint.get("cookies"),
            auth=endpoint.get("auth"),
            timeout=endpoint.get("timeout"),
            allow_redirects=endpoint.get("allow_redirects", True),
            verify=endpoint.get("verify", True),
            stream=endpoint.get("stream", False),
        )

        return Response(
            method=method,
            url=str(response.url),
            http_version=f"HTTP/{response.raw.version / 10}",
            status_code=response.status_code,
            headers=dict(response.headers),
            content=response.content,
        )
