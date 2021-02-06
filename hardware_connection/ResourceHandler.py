from simple_rest_client.exceptions import ServerError, NotFoundError

from Resources import GamesResource, PlayersResource, EventsResource, MapResource, RobotsResource, ConsumersResource
from urllib.parse import quote_plus
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
		return self.api.games.get_games().body

	def get_players(self, game_id):
		"""
		This function returns all active players in the given (game_id) game.
		:param game_id: the game identifier
		:return: the player ids of all active players
		"""
		return self.api.players.get_players(game_id).body

	def get_player(self, game_id, player_id):
		"""
		This function returns information about the given player in the given game.
		:param player_id:
		:param game_id: the game identifier
		:return: information about the given player
		"""
		return self.api.players.get_player(game_id, player_id).body

	def get_controlled_entities(self, game_id, player_id):
		"""

		:param game_id:
		:param player_id:
		:return:
		"""
		return self.api.players.get_player(game_id, player_id)["controlledEntities"].body

	def get_game_state(self, game_id, user_token):
		"""
		This function returns the current state of the given game.
		:param user_token:
		:param game_id: the game identifier
		:return: state of the game
		"""
		return self.api.games.get_game_status(game_id, user_token).body["state"]

	def create_consumer(self, game_id):
		"""
		This function registers an consumer for hardware interaction.
		:param game_id: the game identifier
		:return: Response from the server e.g. the pat and the id
		"""
		return self.api.consumers.create_consumer(game_id, body={"name": "REST_consumer",
																 "description": "Consumes the REST API"}).body

	def check_if_consumer_is_registered(self, game_id, user_token):
		"""
		This function checks if a consumer is registered before the game starts. Otherwise the game needs to be
		restarted.
		:param game_id: the game identifier
		:param user_token: the consumer token
		"""
		while True:
			try:
				self.api.events.get_event_head(game_id, quote_plus(user_token)).body["type"]
			except ServerError as ex:
				print(ex.__str__())
				print("You have no active consumer on the current game. \nYou need to restart the game!")
			except NotFoundError as ex_n:
				print("Caught exception {}".format(ex_n.__str__()))
			time.sleep(2)

	def get_event_head(self, game_id, user_token):
		"""
		This functions returns the event head message from the API endpoint.
		:param game_id: the game identifier
		:param user_token: the consumer token
		:return:
		"""
		return self.api.events.get_event_head(game_id, user_token)

	def get_new_games(self, current_games):
		"""
		This function compares the current games with the new games and
		builds the difference.
		:param current_games: a list of all current games
		:return: the difference
		"""
		new_games = self.get_games()
		return list(set(new_games) ^ set(current_games))
