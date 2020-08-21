from __future__ import annotations
# Python built-in imports
import asyncio

from http import HTTPStatus
from typing import List

# Site-package imports
from aiohttp import ClientTimeout, ClientSession
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class Domain(object):
	""" Convenience class for storing values and functions required (helpful)
		for ripping favicons.

		:param rank: Initialize objects with their CSV rank
		:param url: Domain URL e.g google.com
	"""
	def __init__(self, rank: int, url: str) -> None:
		self.rank = rank
		self.url = url
		self.favicon_url = None
		self.error_message = None


	def __lt__(self, other: Domain) -> bool:
		"""	Allows sorting based on rank
			
			:param other: Domain
		"""
		return int(self.rank) < int(other.rank)

	@classmethod
	async def fetch_from_domain(
		cls,
		domain: Domain,
		session: ClientSession) -> None:
		""" Check a domains standard favicon URL location. If found,
			set the favicon_url variable.

			:param domain: 	Domain object to check
			:param session: ClientSession for making requests
		"""

		favicon_url = None

		try:
			response = await session.get(f"http://{domain.url}/favicon.ico")
			# Cheeky way to handle redirects
			favicon_url = response.url.__str__()
			domain.favicon_url = favicon_url
		except (asyncio.TimeoutError) as e: # Timeout has no string :shruggie:
			domain.error_message = f"{e.__class__.__name__}"
		except Exception as e:
			domain.error_message = f"{e.__class__.__name__}: {str(e)}"


	@classmethod
	async def search_domain_for_favicon(
		cls,
		domain: Domain,
		session: ClientSession) -> None:
		""" Parse a domains HTML for favicon link relations which often
			have the attribute "icon" or "shortcut icon". If found,
			set the domains favicon_url variable

			:param domain: 	Domain object to check
			:param session: ClientSession for making requests
		"""

		favicon_url = None

		try:
			response = await session.get(f"http://{domain.url}")
			favicon_url = domain.find_favicon(domain, await response.text())
		except asyncio.TimeoutError as e:
			domain.error_message = f"{e.__class__.__name__}"
		except Exception as e:
			domain.error_message = f"{e.__class__.__name__}: {str(e)}"

		domain.favicon_url = favicon_url

	def find_favicon(
		self, 
		domain: Domain, 
		content: str) -> str:
		""" Parse HTML content for favicon references

			:param domain: 	Domain object to check
			:param content: HTML content from a GET request

			:return str: favicon URL
		"""

		soup = BeautifulSoup(content, "html.parser")

		for rel in ["icon", "shortcut icon"]:
			links = soup.findAll(
				lambda tag: tag.name.lower() == "link",
				rel=lambda attribute: attribute.lower() == rel or attribute.title() == rel,
			)
		if links:
			return urljoin(f"http://{domain.url}", links[0]["href"])

		return None