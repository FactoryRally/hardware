from simple_rest_client.api import API
from ConnectionHandler import ConnectionHandler
from ResourceHandler import ResourceHandler
from REST_Client import RestReceiver
import threading
import time


class Main:
	"""
	This class handles the generation of REST Receivers threads.
	"""
	# The root URL for the REST API
	API_ROOT_URL = "http://localhost:5050/v1/"

	def __init__(self):
		"""
		The init function initiates an API object, a Reosurce and Connection Handler
		and generates a RestReceiver.
		"""
		self.api = API(api_root_url=self.API_ROOT_URL, json_encode_body=True)
		self.resource_handler = ResourceHandler(self.api)
		self.resource_handler.add_resources()
		self.connection_handler = ConnectionHandler(self.api)
		self.connection_handler.wait_for_api_availability()
		games = self.resource_handler.get_games()
		self.threads = []
		self.generate_threads(games)

	def generate_threads(self, games):
		"""
		This function
		:param games:
		:return:
		"""
		for a in games:
			print(a)
			t = threading.Thread(target=self.generate_games(a))
			t.start()
			self.threads.append(t)

	def generate_games(self, game_id):
		"""
		This function generates REST Receivers for each game thats currently running ("LOBBY" status).
		:return:
		"""
		return RestReceiver(self.resource_handler, self.connection_handler, game_id)

	def check_for_new_games(self):
		"""
		This
		:return:
		"""
		while True:
			new_games = self.resource_handler.get_new_games()
			if new_games:
				self.generate_threads(new_games)
			time.sleep(5)


if __name__ == '__main__':
	Main()
