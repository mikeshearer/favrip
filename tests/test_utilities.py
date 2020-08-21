# Python built-in imports
from collections import Awaitable

# Site-package imports
import pytest

from asyncio import Semaphore

# Relative imports
from favrip.utilities import bind


async def _async_dummy():
	return None

@pytest.mark.asyncio
async def test_bind():
	semaphore = Semaphore(10)
	bound_function = bind(semaphore, _async_dummy())

	assert isinstance(bound_function, Awaitable)