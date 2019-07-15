import asyncio
import json
import threading
import time

import pytest
import yaml
from uvicorn import Config, Server


class TestServer(Server):
    @property
    def address(self):
        return f"http://{self.config.host}:{self.config.port}"

    def install_signal_handlers(self):
        pass


async def app(scope, receive, send):
    await send({"type": "http.response.start", "status": 200})
    await send(
        {"type": "http.response.body", "body": json.dumps(scope, default=str).encode()}
    )


@pytest.fixture(scope="function")
def config(tmpdir):
    def configure(data):
        path = tmpdir.join("cfg.yml")
        path.write(yaml.dump(data=data, default_flow_style=False))
        return path

    yield configure


@pytest.fixture(scope="session")
def server():
    config = Config(app=app, loop="asyncio", lifespan="off", port=8001)
    server = TestServer(config=config)
    thread = threading.Thread(target=server.run)
    try:
        thread.start()
        while not server.started:
            time.sleep(0.01)
        yield server
    finally:
        server.should_exit = True
        thread.join()
        asyncio.get_event_loop().run_until_complete(server.shutdown())
