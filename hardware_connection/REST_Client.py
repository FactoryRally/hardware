from urllib.parse import quote
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
	EXECUTION_PHASE = False
	topic = "general"

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
		self.user_token = quote(str(self.resource_handler.create_consumer(self.game_id)["pat"]))
		print(self.user_token)
		if self.resource_handler.get_game_state(self.game_id) != self.PLAYING_STATE:
			self.connection_handler.wait_for_running_game(self.game_id, self.resource_handler)
		self.players = self.resource_handler.get_players(self.game_id, self.user_token)
		print(self.resource_handler.get_game_state(self.game_id))
		self._controlled_entities = {}
		self.generate_entity_mapping()
		print(self._controlled_entities)

	def generate_entity_mapping(self):
		"""
		This function generates a dictionary containing the player id and the corresponding controlled entity.
		:return: dict of entity mapping
		"""
		mapping = {}
		for player in self.players:
			mapping[self.resource_handler.get_controlled_entities(self.game_id, player, self.user_token)] = player

		self._controlled_entities = mapping

	def get_current_message(self):
		"""
		This function returns the latest (pop) game event message (JSON).
		:return: current message
		"""

		if self.resource_handler.get_game_state(self.game_id):
			try:
				msg = self.resource_handler.get_event_head(self.game_id, self.user_token)
				print(msg)
				if str(msg).__contains__("server_error"):
					print("HERE SERVER")
					return None
				elif msg is None:
					print("HERE Not Found")
					return None
				if self.check_if_all_player_have_entity() and self.check_if_event_is_action(msg):
					self.topic = self.evaluate_correct_topic(msg)
				return list([msg, self.topic])
			except NotFoundError as ex_n:
				print("Caught exception {}".format(ex_n.__str__()))

	def evaluate_correct_topic(self, msg):
		"""
		This function returns the corresponding topic of the given message.
		"""
		return self._controlled_entities[msg.entityID]

	def get_controlled_entities(self):
		"""
		This
		:return:
		"""
		return self._controlled_entities

	def check_if_all_player_have_entity(self):
		"""
		This
		:return:
		"""
		return len(self._controlled_entities) == len(self.players)

	def check_if_event_is_action(self, msg):
		if not dict(msg).__contains__('entityID'):
			return False


if __name__ == '__main__':
	RestReceiver(None, None, None)
