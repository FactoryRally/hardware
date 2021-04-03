from simple_rest_client.resource import Resource

"""
This module provides resources, aka an abstraction method for each endpoint. 
"""


class GamesResource(Resource):
	"""
	This class represents all resources which represent the games endpoint.
	"""
	actions = {
		"get_games": {"method": "GET", "url": "games"},  # Used to get game meta information
		"get_game_status": {"method": "GET", "url": "games/{}/status"},  # Get the status of the running game
		"get_game_actions": {"method": "GET", "url": "games/{}/actions"}  # Get game actions (no actions related to
		# Players are returned)
	}


class PlayersResource(Resource):
	"""
	This class represents all resources which represent the players endpoint.
	"""
	actions = {
		"get_players": {"method": "GET", "url": "games/{}/players?pat={}"},  # Get all connected players
		"get_player": {"method": "GET", "url": "games/{}/players/{}?pat={}"},  # Get the player information - controlled
		# entities (robots)
	}


class ConsumersResource(Resource):
	"""
	This class represents all resources which represent the consumer endpoint.
	"""
	actions = {
		"create_consumer": {"method": "POST", "url": "games/{}/consumers"}
	}


class EventsResource(Resource):
	"""
	This class represents all resources which represent the event handling endpoint.
	"""
	actions = {
		"get_event_head": {"method": "GET", "url": "games/{}/events/head?pat={}"},
		# Get the latest event - you receive all events over this endpoint
	}


class RobotsResource(Resource):
	"""
	This class represents all resources which represent the robots endpoint.
	"""
	actions = {
		"get_all_robots": {"method": "GET", "url": "games/{}/entities/robots?pat={}"},  # Get all given robots
		"get_upgrades": {"method": "GET", "url": "games/{}/entities/robots/{}/upgrades"},
		# Get the upgrades of a certain robot
		"get_robot_info": {"method": "GET", "url": "games/{}/entities/robots/{}/info"},
		# Get information about a certain robot
	}


class MapResource(Resource):
	"""
	This class represents all resources which represent the maps endpoint.
	"""
	actions = {
		"get_map": {"method": "GET", "url": "games/{}/map"},  # Receive map info
	}
