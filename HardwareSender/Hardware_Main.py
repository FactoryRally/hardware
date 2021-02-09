from simple_rest_client.api import API
from ResourceHandler import ResourceHandler
from ConnectionHandler import ConnectionHandler
from REST_Client import RestReceiver
from sender import MQTTSender
import time


class HardwareMain:
	"""
	This class initiates the REST Receiver and the MQTT Sender and
	starts the game process.
	"""
	# The root URL for the REST API
	API_ROOT_URL = "http://localhost:5050/v1/"

	def __init__(self):
		"""
		This init function
		"""
		self.api = API(api_root_url=self.API_ROOT_URL, json_encode_body=True)
		self.resource_handler = ResourceHandler(self.api)
		self.resource_handler.add_resources()
		self.connection_handler = ConnectionHandler(self.api)
		self.connection_handler.wait_for_api_availability()
		self.connection_handler.wait_for_initialized_game()
		self.games = self.resource_handler.get_games()
		self.check_for_lobby_game()
		self.threads = []
		self.generate_threads(self.games)
		self.check_for_new_games()

	def generate_threads(self, games):
		"""
		This function generates a REST Receiver thread for each game.
		:param games: a list of the current games (or newly added ones)
		"""
		for game in games:
			print(game)
			new_game = self.generate_game(game)
			print("THREAD CREATED!")
			t = MQTTSender(new_game)
			t.run()
			self.threads.append(t)

	def generate_game(self, game_id):
		"""
		This function generates REST Receivers for each game thats currently running ("LOBBY" status).
		:return: a REST Receiver Instance
		"""
		return RestReceiver(self.resource_handler, self.connection_handler, game_id)

	def check_for_new_games(self):
		"""
		This function checks each 5 seconds if a new game was added - if
		there was one added, a new thread for handling this game (if it
		meets the criteria) is initiated.
		:return:
		"""
		while True:
			new_games = self.resource_handler.get_new_games(self.games)
			if new_games:
				self.generate_threads(new_games)
				self.games = new_games
			time.sleep(5)

	def check_for_lobby_game(self):
		if not self.games:
			print("You need to start a game! There are only FINISHED matches running!")


if __name__ == '__main__':
	HardwareMain()
