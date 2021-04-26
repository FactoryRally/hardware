import requests
import time

"""
This module is handling connection issues and checks.
"""


class ConnectionHandler:
	"""
	This class handles the connection to the API and manages different possible errors as well as it performs checks.
	"""
	game_started = "PLAYING"

	def __init__(self, api, api_root_url):
		"""
		The init function takes the api as an argument and initiates the object.
		:param api: an API instance
		"""
		self.api = api
		self.api_root_url = api_root_url

	def wait_for_running_game(self, game_id, resource_handler):
		"""
		This function waits until a game is started.
		:param game_id: the given game
		:param resource_handler: the resource handler
		"""
		while resource_handler.get_game_state(game_id) != self.game_started:
			print(f"[{game_id}]: Game has not started yet!")
			time.sleep(3)
		return

	def wait_for_initialized_game(self):
		"""
		This function waits until at least one game is initialized.
		"""
		while not self.api.games.get_games().body:
			print("No game has been initialized")
			time.sleep(3)
		return

	def wait_for_api_availability(self):
		"""
		This function waits until the API is reachable.
		"""
		while True:
			try:
				resp = requests.get(self.api_root_url.strip("/v1")+"/swagger/index.html")
				resp.raise_for_status()
				return
			except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
				print("URL is not up. Please start the game-server!")
			except requests.exceptions.HTTPError:
				print(self.api_root_url.strip("/v1"))
				print("HTTP Server Error! Please restart the Server!")
			time.sleep(3)