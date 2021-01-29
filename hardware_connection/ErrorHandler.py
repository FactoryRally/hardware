import time,requests

class ErrorHandler:
	safe_url = "http://localhost:5050/swagger/index.html"

	def __init__(self,api):
		self.api = api

	def wait_for_initialized_game(self):
		while True:
			try:
				self.api.games.get_game().body[0]
				return
			except (IndexError,TypeError):
				print("Game has not been initialized")
				time.sleep(1)

	def wait_for_internet_connection(self):
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
