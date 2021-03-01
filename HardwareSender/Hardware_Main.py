from simple_rest_client.api import API
from REST.ResourceHandler import ResourceHandler
from REST.ConnectionHandler import ConnectionHandler
from REST.RESTClient import RestReceiver
from MQTT.MQTTPublisher import MQTTPublisher
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
		self.game_id = gui.value
		self.game = self.generate_game(game_id=self.game_id)
		publisher = MQTTPublisher(self.game)
		publisher.start()

	def generate_game(self, game_id):
		"""
		This function generates REST Receivers for each game thats currently running ("LOBBY" status).
		:return: a REST Receiver Instance
		"""
		return RestReceiver(self.resource_handler, self.connection_handler, game_id)


if __name__ == '__main__':
	HardwareMain()
