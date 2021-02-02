import requests
import time


class ConnectionHandler:
	"""
	This class handles the connection to the API and manages different possible errors as well as it performs checks.
	"""
	safe_url = "http://localhost:5050/"

	def __init__(self, api):
		"""
		The init function takes the api as an argument and initiates the object.
		:param api: the API
		"""
		self.api = api
		self.game_started = 0

	def wait_for_running_game(self, game_id, resource_handler):
		"""
		This function waits until a game is started.
		:param game_id: the given game
		:param resource_handler: the resource handler
		:return:
		"""
		while resource_handler.get_game_state(game_id) != self.game_started:
			print("Not started")
			time.sleep(1)
		return

	def wait_for_initialized_game(self):
		"""
		This function waits until a game is initialized.
		:return:
		"""
		while not self.api.games.get_game().body:
			print("Game has not been initialized")
			time.sleep(1)
		return

	def wait_for_api_availability(self):
		"""
		This function waits until the API is reachable. 
		:return:
		"""
		while True:
			try:
				resp = requests.get(self.safe_url)
				resp.raise_for_status()
				return
			except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
				print("URL is not up. Please start the game-server!")
			except requests.exceptions.HTTPError:
				print("4xx, 5xx")
			time.sleep(1)
