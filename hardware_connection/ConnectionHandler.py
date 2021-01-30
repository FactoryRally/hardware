import requests
import time


class ConnectionHandler:
	"""
	This
	"""
	safe_url = "http://localhost:5050/"

	def __init__(self,api):
		self.api = api

	def wait_for_initialized_game(self):
		while True:
			try:
				time.sleep(1)
				self.api.games.get_game().body[0]
				return
			except (IndexError,TypeError):
				print("Game has not been initialized")

	def wait_for_api_availability(self):
		while True:
			try:
				time.sleep(1)
				resp = requests.get(self.safe_url)
				resp.raise_for_status()
				return
			except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
				print("Down")
				pass
			except requests.exceptions.HTTPError:
				print("4xx, 5xx")
				pass
