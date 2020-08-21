# Python built-in imports
from asyncio import Semaphore
from collections import Awaitable, Coroutine


async def bind(sem: Semaphore, coroutine: Coroutine) -> Awaitable:
	"""	Wrap a function in a "bottleneck" (read: semaphore).
		This ensures that only X number of instances of this function
		can be run at a time.

		:param sem: 		Instantiated sempahore
		:param coroutine:	Reference to a called asynchronous function

		:return Awaitable: 	Awaitable function reference
	"""
	async with sem:
		return await coroutine