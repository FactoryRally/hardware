from Resources import GamesResource, PlayersResource, EventsResource, MapResource, RobotsResource, ConsumersResource

class ResourceHandler:
	"""
	This
	"""
	def __init__(self,api):
		self.api = api

	def add_resources(self):
		self.api.add_resource(resource_name='games', resource_class=GamesResource)
		self.api.add_resource(resource_name='players', resource_class=PlayersResource)
		self.api.add_resource(resource_name='events', resource_class=EventsResource)
		self.api.add_resource(resource_name='maps', resource_class=MapResource)
		self.api.add_resource(resource_name='robots', resource_class=RobotsResource)
		self.api.add_resource(resource_name='consumers', resource_class=ConsumersResource)

	def get_game(self):
		return self.api.games.get_game().body[0]

	def get_players(self,game_id):
		return self.api.players.get_players(game_id).body

	def get_player(self,game_id):
		return self.api.players.get_player(game_id, self.api.players.get_players(game_id).body)

	def get_game_state(self,game_id):
		return self.api.games.get_game_status(game_id).body["state"]

	def create_consumer(self,game_id):
		return self.api.consumers.create_consumer(game_id, body={"name": "REST_consu23", "description": "Consumes the REST API"}).body