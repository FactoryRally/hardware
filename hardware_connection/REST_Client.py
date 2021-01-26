from simple_rest_client.api import API
from Resources import GamesResource, PlayersResource, EventsResource, MapResource, RobotsResource


class RestReceiver:
	"""
	This class provides the interface between the REST API and
	the Raspberry Pi, which retrieves the data.
	"""

	# The root URL for the REST API
	api_root_url = "http://localhost:5050/v1"
	# The different Event Types
	event_types = [
		"movement", "upgrade purchase", "fill register", "activate upgrade", "lazer shot",
		"game start", "clear shop", "fill shop", "register clear", "programming timer start",
		"programming timer stop", "random card distribution", "take card event", "activate checkpoint",
		"game_phase_changed", "game_round_phase_changed", "pause", "unpause", "damage", "lazer hit",
		"push", "join", "lock in", "robot_start_executing", "heal", "energy gain"
	]

	def __init__(self):
		"""

		"""
		self.api = API(api_root_url=self.api_root_url, json_encode_body=True)
		self.add_resources()
		self.init_game()
		status = self.get_game_status()
		print(status)
		if status["state"] == 0:
			self.start_game()

	def get_game(self):
		return self.api.games.get_game().body[0]

	def get_players(self):
		return self.api.players.get_players(self.game_id).body

	def get_player(self):
		return self.api.players.get_player(self.game_id, self.api.players.get_players(self.game_id).body)

	def get_game_status(self):
		return self.api.games.get_game_status(self.game_id).body

	def add_resources(self):
		self.api.add_resource(resource_name='games', resource_class=GamesResource)
		self.api.add_resource(resource_name='players', resource_class=PlayersResource)
		self.api.add_resource(resource_name='events', resource_class=EventsResource)
		self.api.add_resource(resource_name='maps', resource_class=MapResource)
		self.api.add_resource(resource_name='robots', resource_class=RobotsResource)

	def init_game(self):
		self.game_id = self.get_game()
		self.players = self.get_players()

	def start_game(self):
		print("Starte Spielablauf")


if __name__ == '__main__':
	RestReceiver()
