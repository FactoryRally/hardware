from simple_rest_client.api import API
from ConnectionHandler import *
from ResourceHandler import ResourceHandler

class Main:
	api_root_url = "http://localhost:5050/v1/"

	def __init__(self):
		self.api = API(api_root_url=self.api_root_url, json_encode_body=True)
		self.resource_handler = ResourceHandler(self.api)
		self.connection_handler =
