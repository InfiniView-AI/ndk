import json

from aiohttp import web
from src.back.server import broadcast
import pytest

@pytest.fixture
def cli(loop, aiohttp_client):
    app = web.Application()
    app.router.add_post('/broadcast', broadcast)
    app.router.add_options('/broadcast', broadcast)
    return loop.run_until_complete(aiohttp_client(app))

@pytest.mark.asyncio
async def test_broadcast_options(cli):
    response = await cli.options('/broadcast')
    assert response.status == 200


@pytest.mark.asyncio
async def test_broadcast_post(cli):
    sample_request_data = {
        "sdp": "my-sample-sdp",
        "type": "offer",
    }
    resp = await cli.post('/broadcast', data=json.dumps(sample_request_data))
    assert resp.status == 200
    response_data = await resp.json()
    assert "sdp" in response_data and "type" in response_data

@pytest.mark.asyncio
async def test_broadcast_empty_body_post(cli):
    empty_request_data = {}
    resp = await cli.post('/broadcast', data=json.dumps(empty_request_data))
    assert resp.status == 400
