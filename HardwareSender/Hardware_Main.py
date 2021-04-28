from simple_rest_client.api import API

from GUI.InputIP import InputIP
from NetworkUtilities.GameScan import check_subnet_for_open_port
from REST.ResourceHandler import ResourceHandler
from REST.ConnectionHandler import ConnectionHandler
from MQTT.MQTTPublisher import MQTTPublisher
from GUI import GameGUI
from GUI.GameGUI import GameGUI

"""
This module is the entrypoint for the application, initializing all components and providing a reset method
for game end (new game start). 
"""


def make_ip_functional(ip):
	"""
	This
	:param ip:
	:return:
	"""
	return "http://"+ip+":5050/v1"


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
		api_root_url = make_ip_functional("192.168.0.132")
		self.api = API(api_root_url=api_root_url, json_encode_body=True)
		self.resource_handler = ResourceHandler(self.api, api_root_url)
		self.setup_resource_handler()
		self.connection_handler = ConnectionHandler(self.api, api_root_url)
		self.setup_connection_handler()
		self.games = self.resource_handler.get_games()
		self.resource_handler.check_for_lobby_game(self.games)
		self.gui = GameGUI(self)
		self.gui.mainloop()
		sel = self.gui.get_game()
		MQTTPublisher(self.gui, self, self.connection_handler, self.resource_handler, sel)

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


if __name__ == '__main__':
	HardwareMain()
