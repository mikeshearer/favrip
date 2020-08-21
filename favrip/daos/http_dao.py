# Site package imports
from aiohttp import (
	AsyncResolver,
	ClientSession,
	ClientResponse,
	ClientTimeout,
	DummyCookieJar,
	TCPConnector)

import socket

# Globals
HEADERS = {
	'Accept': '*/*',
	'Connection': 'keep-alive',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
	'Accept-Encoding': 'gzip',
	'Accept-Language': 'en-US;q=0.5,en;q=0.3',
	'Cache-Control': 'max-age=0',
	'DNT': '1',
	'Upgrade-Insecure-Requests': '1'
}

DNS_NAMESERVERS = ["8.8.8.8", "8.8.4.4"]


class HTTPDao(object):
	""" DAO for accessing data through HTTP requests """

	@classmethod
	def create_session(
		cls,
		connector: TCPConnector = None,
		timeout: int = 5,
		headers: dict = None) -> ClientSession:
		"""	Create and return an aiohttp ClientSession with default or
			some custom parameters.

			:param connector: Connector for standard TCP Sockets
			:param timeout: Maximum time to wait for an HTTP response
			:param headers: Spoofed request headers to trick some websites

			:return session: Session ready to go
		"""
		resolver = AsyncResolver(
			nameservers=DNS_NAMESERVERS)
		connector = TCPConnector(
			limit=100,
			limit_per_host=0,
			resolver=resolver if resolver else cls.create_resolver(),
			use_dns_cache=False,
			force_close=True,
			family=socket.AF_INET,
			ssl=False)
		session = ClientSession(
			cookie_jar=DummyCookieJar(),
			connector=connector,
			timeout=ClientTimeout(total=timeout),
			headers=HEADERS,
			connector_owner=True
		)
		return session
