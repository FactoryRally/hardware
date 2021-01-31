from simple_rest_client.resource import Resource


class GamesResource(Resource):
	"""
	This
	"""
	actions = {
		"get_game": {"method": "GET", "url": "games"},  # Used to get game meta information
		"get_game_status": {"method": "GET", "url": "games/{}/status"},  # Get the status of the running game
		"get_game_actions": {"method": "GET", "url": "games/{}/actions"}  # Get game actions (no actions related to
		# Players are returned)
	}


class PlayersResource(Resource):
	"""
	This
	"""
	actions = {
		"get_players": {"method": "GET", "url": "games/{}/players"},  # Get all connected players
		"get_player": {"method": "GET", "url": "games/{}/players/{}"},  # Get the player information - controlled
		# entities (robots)
	}


class ConsumersResource(Resource):
	"""
	This
	"""
	actions = {
		"create_consumer": {"method": "POST", "url": "games/{}/consumers"}
	}


class EventsResource(Resource):
	"""
	This
	"""
	actions = {
		"get_event_head": {"method": "GET", "url": "games/{}/events/head?pat={}"},
		# Get the latest event - you receive all events over this endpoint
	}


class RobotsResource(Resource):
	"""
	This
	"""
	actions = {
		"get_all_robots": {"method": "GET", "url": "games/{}/entitys/robots"},  # Get all given robots
		"get_upgrades": {"method": "GET", "url": "games/{}/entitys/robots/{}/upgrades"},
		# Get the upgrades of a certain robot
		"get_robot_info": {"method": "GET", "url": "games/{}/entitys/robots/{}/info"},
		# Get information about a certain robot
	}


class MapResource(Resource):
	"""
	This
	"""
	actions = {
		"get_map": {"method": "GET", "url": "games/{}/map"},  # Receive map info
	}
