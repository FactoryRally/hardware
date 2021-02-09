from simple_rest_client.exceptions import ServerError, NotFoundError
from Resources import GamesResource, PlayersResource, EventsResource, MapResource, RobotsResource, ConsumersResource
import sys
import time


class ResourceHandler:
	"""
	This class provides functions for interaction with the API resources.
	"""

	def __init__(self, api):
		"""
		The init function takes the api as an argument and initiates the object.
		:param api: the API
		"""
		self.api = api
		self.add_resources()

	def add_resources(self):
		"""
		This function connects the API with the resources.
		"""
		self.api.add_resource(resource_name='games', resource_class=GamesResource)
		self.api.add_resource(resource_name='players', resource_class=PlayersResource)
		self.api.add_resource(resource_name='events', resource_class=EventsResource)
		self.api.add_resource(resource_name='maps', resource_class=MapResource)
		self.api.add_resource(resource_name='robots', resource_class=RobotsResource)
		self.api.add_resource(resource_name='consumers', resource_class=ConsumersResource)

	def get_games(self):
		"""
		This function returns all currently active games.
		:return: the game ids of all active games
		"""
		active_games = list(self.api.games.get_games().body)
		for a in active_games:
			if self.get_game_state(a) == 'FINISHED':
				active_games.remove(a)
		return active_games

	def get_players(self, game_id, user_token):
		"""
		This function returns all active players in the given (game_id) game.
		:param user_token: the given consumer access token
		:param game_id: the given game identifier
		:return: the player ids of all active players
		"""
		return self.api.players.get_players(game_id, user_token).body

	def get_player(self, game_id, player_id):
		"""
		This function returns information about the given player in the given game.
		:param player_id: the given player id
		:param game_id: the given game identifier
		:return: information about the given player
		"""
		return self.api.players.get_player(game_id, player_id).body

	def get_controlled_entities(self, game_id, player_id, user_token):
		"""
		This method returns the controlled entities of the given player.
		:param user_token: the given consumer access token
		:param game_id: the given game identifier
		:param player_id: the given player id
		:return: the id of the controlled robot from the given player
		"""
		return self.api.players.get_player(game_id, player_id, user_token).body['controlled_entities'][0]

	def get_game_state(self, game_id):
		"""
		This method returns the current state of the given game.
		:param game_id: the given game identifier
		:return: state of the game
		"""
		try:
			return self.api.games.get_game_status(game_id).body["state"]
		except NotFoundError:
			print(f"[{game_id}]: GAME not found")

	def create_consumer(self, game_id):
		"""
		This method registers an consumer for hardware interaction.
		:param game_id: the given game identifier
		:return: Response from the server e.g. the pat and the id
		"""
		return self.api.consumers.create_consumer(game_id, body={"name": "RESTConsumer", "description": "Consumes the REST API"}).body

	def get_event_head(self, game_id, user_token):
		"""
		This method returns the event head message from the API endpoint.
		:param game_id: the given game identifier
		:param user_token: the given consumer access token
		:return: the latest event
		"""
		try:
			return self.api.events.get_event_head(game_id, user_token).body
		except NotFoundError as e:
			print(f"[{game_id}]: {e.__str__()}")
		except ServerError:
			print(f"[{game_id}]: Server Error! Please restart Server!")
			sys.exit()

	def get_new_games(self, current_games):
		"""
		This method compares the current games with the new games and
		builds the difference.
		:param current_games: a list of all current games
		:return: the difference between all current games and the given games
		"""
		new_games = self.get_games()
		return list(set(new_games) ^ set(current_games))

	def get_all_robots(self, game_id, user_token):
		"""
		This method returns all robot ids.
		:param game_id: the given game identifier
		:param user_token: the given consumer access token
		:return: all robot ids
		"""
		return self.api.robots.get_all_robots(game_id, user_token)

	def check_for_lobby_game(self, games):
		"""
		This method waits until there are games in LOBBY state.
		:param games: all game ids that are currently active
		"""
		while not games:
			print("You need to start a game! There are only FINISHED matches running!")
			time.sleep(3)
