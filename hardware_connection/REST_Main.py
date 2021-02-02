from simple_rest_client.api import API
from ConnectionHandler import *
from ResourceHandler import ResourceHandler
from REST_Client import RestReceiver


class Main:
	"""
	This class handles the generation of REST Receivers threads.
	"""
	api_root_url = "http://localhost:5050/v1/"

	def __init__(self):
		self.api = API(api_root_url=self.api_root_url, json_encode_body=True)
		self.resource_handler = ResourceHandler(self.api)
		self.connection_handler = ConnectionHandler(self.api)
		self.generate_games()

	def generate_games(self):
		"""
		This function generates REST Receivers for each game thats currently running ("LOBBY" status).
		:return:
		"""
		return RestReceiver(self.api, self.resource_handler, self.connection_handler)


if __name__ == '__main__':
	Main()
