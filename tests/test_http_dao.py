import pytest

from aiohttp import ClientSession

from favrip.daos.http_dao import HTTPDao

@pytest.mark.asyncio
async def test_create_session():
	session = HTTPDao.create_session()

	assert isinstance(session, ClientSession)
