from urllib.parse import quote_plus
import time
from simple_rest_client.exceptions import NotFoundError


class RestReceiver:
	"""
	This class provides the interface between the REST API and
	the Raspberry Pi, which retrieves and processes the data.
	"""

	# The different Event Types
	event_types = [
		"movement", "upgrade purchase", "fill register", "activate upgrade", "lazer shot",
		"game start", "clear shop", "fill shop", "register clear", "programming timer start",
		"programming timer stop", "random card distribution", "take card event", "activate checkpoint",
		"game_phase_changed", "game_round_phase_changed", "pause", "unpause", "damage", "lazer hit",
		"push", "join", "lock in", "robot_start_executing", "heal", "energy gain"
	]
	# state of game
	PLAYING_STATE = "PLAYING"

	def __init__(self, res, conn, game_id):
		"""
		This function initializes the REST client and the game. Furthermore it performs checks if the game is in the
		right state and registers a consumer to consume the event endpoint.
		"""
		self.resource_handler = res
		self.connection_handler = conn
		self.connection_handler.wait_for_api_availability()
		self.connection_handler.wait_for_initialized_game()

		self.game_id = game_id
		self.players = self.resource_handler.get_players(self.game_id)
		self.user_token = quote_plus(str(self.resource_handler.create_consumer(self.game_id)["pat"]))
		if self.resource_handler.get_game_state(self.game_id, self.user_token) != self.PLAYING_STATE:
			self.connection_handler.wait_for_running_game(self.game_id, self.resource_handler, self.user_token)
		print(self.resource_handler.get_game_state(self.game_id, self.user_token))
		self.resource_handler.check_if_consumer_is_registered(self.game_id, self.user_token)

	def start_game(self):
		"""
		This function starts the game process and handles interaction.
		:return:
		"""
		while True:
			try:
				print(self.resource_handler.get_event_head(self.game_id, self.user_token))
			except NotFoundError as ex_n:
				print("Caught exception {}".format(ex_n.__str__()))
				time.sleep(1)


if __name__ == '__main__':
	RestReceiver()
