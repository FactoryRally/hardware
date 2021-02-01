from simple_rest_client.api import API
from ConnectionHandler import *
from ResourceHandler import ResourceHandler
from urllib.parse import urlencode

# AWAIT testen ob ähnlich wie while T

class RestReceiver:
	"""
	This class provides the interface between the REST API and
	the Raspberry Pi, which retrieves and processes the data.
	"""

	# The root URL for the REST API
	api_root_url = "http://localhost:5050/v1/"
	# The different Event Types
	event_types = [
		"movement", "upgrade purchase", "fill register", "activate upgrade", "lazer shot",
		"game start", "clear shop", "fill shop", "register clear", "programming timer start",
		"programming timer stop", "random card distribution", "take card event", "activate checkpoint",
		"game_phase_changed", "game_round_phase_changed", "pause", "unpause", "damage", "lazer hit",
		"push", "join", "lock in", "robot_start_executing", "heal", "energy gain"
	]
	game_started = 0

	def __init__(self):
		"""
		This function initializes the REST client and the game as well as it starts the whole
		method.
		"""
		self.api = API(api_root_url=self.api_root_url, json_encode_body=True)
		resource_handler = ResourceHandler(self.api)
		resource_handler.add_resources()
		connection_handler = ConnectionHandler(self.api)
		connection_handler.wait_for_api_availability()
		connection_handler.wait_for_initialized_game()

		self.game_id = resource_handler.get_game()
		print(self.game_id)
		self.players = resource_handler.get_players(self.game_id)
		status = resource_handler.get_game_state(self.game_id)
		print(status)
		user_token = resource_handler.create_consumer(self.game_id)
		connection_handler.wait_for_running_game(self.game_id,resource_handler)
		self.start_game(user_token["pat"])

	def start_game(self,token):
		while True:
			print(self.api.events.get_event_head(self.game_id,token))


if __name__ == '__main__':
	RestReceiver()
