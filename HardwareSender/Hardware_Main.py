from simple_rest_client.api import API
from REST.ResourceHandler import ResourceHandler
from REST.ConnectionHandler import ConnectionHandler
from REST.RESTClient import RestReceiver
from MQTT.MQTTPublisher import MQTTPublisher
import time
from GUI.GameSelector import GameSelector


class HardwareMain:
	"""
	This class initiates the REST Receiver and the MQTT Sender and
	starts the game process.
	"""
	api_root_url = "http://localhost:5050/"

	def __init__(self):
		"""
		This init method initiates the main class which provides the access to the REST API and
		dynamically creates a thread for each game.
		"""
		self.api = API(api_root_url=self.api_root_url, json_encode_body=True)
		self.resource_handler = ResourceHandler(self.api)
		self.resource_handler.add_resources()
		self.connection_handler = ConnectionHandler(self.api)
		self.connection_handler.wait_for_api_availability()
		self.connection_handler.wait_for_initialized_game()
		self.games = self.resource_handler.get_games()
		self.resource_handler.check_for_lobby_game()
		gui = GameSelector()
		gui.mainloop()
		self.game = gui.value
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
			print(f"[Game-ID: {game}]: THREAD CREATED!")
			t = MQTTPublisher(new_game)
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
		"""
		while True:
			new_games = self.resource_handler.get_new_games(self.games)
			if new_games:
				self.generate_threads(new_games)
				self.games = new_games
			time.sleep(5)


if __name__ == '__main__':
	HardwareMain()
