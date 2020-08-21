# Python built-in imports
import asyncio
import time
import timeit

# Site-package imports
import tqdm
from collections import Callable
from datetime import timedelta
from typing import List

# Relative imports
from favrip.daos.http_dao import HTTPDao
from favrip.file_operations import read_csv, write_csv
from favrip.models.domain import Domain
from favrip.utilities import bind


def run(
	csv: str,
	parallelism: int,
	timeout: int,
	output_directory: str
) -> int:
	"""	Primary (non CLI) entry point into favrip. Establishes a set of
		Domain objects and the work required to rip favicons.

		:param csv: 			 Input CSV filename reference
		:param parallelism: 	 Maximum number of concurrent HTTP requests
		:param timeout: 		 Timeout for any single HTTP request
		:param output_directory: Where output files will be written

		:return int: Status code, 0 for successs

	"""
	start_time = timeit.default_timer()

	domains = [Domain(int(item[0]), item[1]) for item in read_csv(csv)]

	for func in [Domain.fetch_from_domain, Domain.search_domain_for_favicon]:
		domains = asyncio.run(search(
			domains=domains,
			func=func,
			parallelism=parallelism,
			timeout=timeout))

	domains.sort() # Sort by __lt__ function (comparing rank)

	print("\nFavicon parsing complete, writing output files...")

	write_csv(
		content=[[domain.rank, domain.url, domain.favicon_url] for domain in domains if domain.favicon_url],
		file=f"favrip-success-{time.strftime('%Y%m%d-%H%M%S')}"
	)
	write_csv(
		content=[[domain.rank, domain.url, domain.error_message] for domain in domains if domain.favicon_url is None],
		file=f"favrip-failed-{time.strftime('%Y%m%d-%H%M%S')}"
	)

	duration = round(timeit.default_timer() - start_time)

	print(
		f"\nTime to rip {len(domains)} domains was: {timedelta(seconds=duration)}\n"
	)

	return 0


async def search(
	domains: List[Domain],
	func: Callable,
	parallelism: int,
	timeout: int) -> List[Domain]:
	""" Call an asynchronous function on all elements in a list of Domains
		while respecting a bottleneck (Semaphore). Updates the Domain
		objects favicon_url in place.
	
		:param domains: 	List of Domain objects
		:param func: 		Function to apply to each Domain in domains
		:param parallelism: Maximum number of concurrent HTTP requests
		:param timeout: 	Timeout for any single HTTP request

		:return domains: List of domains
	"""

	tasks = []
	sessions = []
	semaphore = asyncio.Semaphore(parallelism)

	try:
		for domain in tqdm.tqdm(
			[domain for domain in domains if domain.favicon_url is None],
			desc=f"Creating task-list with method: {func.__name__}"):

			session = HTTPDao.create_session(timeout=timeout)
			sessions.append(session) # Keep a reference to all sessions for closure

			bound_coroutine = bind(semaphore, func(domain, session))
			tasks.append(bound_coroutine)

		for future in tqdm.tqdm(
			asyncio.as_completed(tasks),
			total=len(tasks),
			desc=f"Requesting favicons with method: {func.__name__}"
			):
			_ = await future 
		return domains
	finally:
		[await session.close() for session in sessions]
