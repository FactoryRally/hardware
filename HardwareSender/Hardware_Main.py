from simple_rest_client.api import API
from REST.ResourceHandler import ResourceHandler
from REST.ConnectionHandler import ConnectionHandler
from MQTT.MQTTPublisher import MQTTPublisher
from GUI import GameGUI
from GUI.GameGUI import GameGUI, GameSelector

"""
This module is the entrypoint for the application, initializing all components and providing a reset method
for game end (new game start). 
"""

api_root_url = "http://localhost:5050/v1"


class HardwareMain:
	"""
	This class initiates the REST Receiver and the MQTT Sender and
	starts the game process.
	"""

	def __init__(self):
		"""
		This init method initiates the main class which provides the access to the REST API and
		generates a MQTT Publisher instance.
		"""
		self.api = API(api_root_url=api_root_url, json_encode_body=True)
		self.resource_handler = ResourceHandler(self.api)
		self.setup_resource_handler()
		self.connection_handler = ConnectionHandler(self.api)
		self.setup_connection_handler()
		self.games = self.resource_handler.get_games()
		self.resource_handler.check_for_lobby_game(self.games)
		gui = GameGUI(self)
		gui.mainloop()
		sel = gui.get_game()
		publisher = MQTTPublisher(gui, self, self.connection_handler, self.resource_handler, sel)
		publisher.start()

	def setup_resource_handler(self):
		"""
		This method initializes the resource handler.
		"""
		self.resource_handler.add_resources()

	def setup_connection_handler(self):
		"""
		This method initializes the connection handler.
		"""
		self.connection_handler.wait_for_api_availability()
		self.connection_handler.wait_for_initialized_game()


def reset():
	"""
	This method performs a reset upon game end.
	"""
	obj.__init__()


if __name__ == '__main__':
	obj = HardwareMain()
