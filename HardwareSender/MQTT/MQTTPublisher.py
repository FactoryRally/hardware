from paho.mqtt import client as mqtt_client
import random
import time
import Hardware_Main

from GUI.GameGUI import GameSelector, GameStartPage
from REST.RESTClient import RestReceiver

RELEVANT_ACTIONS = []

class MQTTPublisher:
	"""
	This class is the MQTT Sender which pushes the current game event
	to the broker on the according topic.
	"""

	broker = 'broker.emqx.io'
	port = 1883
	client_id = f'python-mqtt-{random.randint(0, 10000)}'
	topics = []
	ids = []
	GEN_TOPIC = "general"
	SETUP = False
	ACTIVE = False
	GAME_STOP = False

	def __init__(self, gui, connection_handler, resource_handler):
		"""
		This init method initiates the client connection and starts the main
		logic of the sender.
		"""
		self.client = self.connect_mqtt()
		self.connection_handler = connection_handler
		self.resource_handler = resource_handler
		self.ui = gui
		self.perform_game_start()

	def start(self):
		"""
		This method starts the game process.
		:return:
		"""
		self.discover_and_notify()
		self.publish()
		self.client.loop_forever()

	def connect_mqtt(self) -> mqtt_client:
		"""
		This method creates a client connection to the MQTT Broker.
		:return: a client instance
		"""

		def on_connect(client, userdata, flags, rc):
			"""
			This method is the callback for a connection.
			:param client: the client
			:param userdata: the submitted userdata
			:param flags: the submitted connection flags
			:param rc: the response code
			"""
			if rc == 0:
				print(f"[{self.game_id}]: Connected to MQTT Broker!")
			else:
				print(f"[{self.game_id}]: Failed to connect, return code %d\n", rc)

		client = mqtt_client.Client(self.client_id)
		client.on_connect = on_connect
		client.connect(self.broker, self.port)
		return client

	def discover_and_notify(self):
		"""
		This method handles the discovery of all clients in the
		current game.
		"""

		def on_message(client, userdata, msg):
			"""
			This method is the callback which gets called when a
			message is received.
			:param client: the client connection
			:param userdata: the submitted userdata
			:param msg: received message
			"""
			msg_decoded = str(msg.payload.decode())
			if msg_decoded.__contains__("winner"):
				self.client.publish(self.GEN_TOPIC, "game-over")
				self.close_game()
			else:
				if msg.topic == self.GEN_TOPIC:
					print(f"[{self.game_id}]: Received message on general: {msg_decoded}")
				else:
					if not msg_decoded.__contains__('type') and self.SETUP is False:
						print(f"[{self.game_id}]: Received `{msg_decoded}` from `{msg.topic}` topic")
						self.topics.append(eval(msg.payload.decode())[2])
						helper_topic = 1
						if self.RestReceiver.get_controlled_entities() == len(self.topics):
							for x in self.topics:
								self.ids.append(helper_topic)
								helper_topic += 1
								print(f"[{self.game_id}]: {helper_topic}")
								client.publish(x, {"Your client topic is": str(helper_topic)}.__str__())
						self.SETUP = True
						self.ACTIVE = True

		self.client.subscribe(self.GEN_TOPIC)
		self.client.on_message = on_message
		while self.RestReceiver.get_controlled_entities() != len(self.topics):
			continue

	def publish(self):
		"""
		This method publishes the current message to the broker with
		the according topic.
		"""
		while True and self.ACTIVE:
			resp = self.RestReceiver.get_current_message()
			if resp is not None:
				msg = resp[0]
				curr_topic = resp[1]
				if str(msg).__contains__("winner"):
					self.GAME_STOP = True
					self.ui.show_frame(self.ui.frames[GameStartPage])
					Hardware_Main.reset()
				if evaluate_relevance(msg) and not self.GAME_STOP:
					result = self.client.publish(curr_topic, str(msg))
					result: [0, 1]
					status = result[0]
					if status == 0:
						print(f"[{self.game_id}]: Send `{msg}` to `{curr_topic}`")
					else:
						print(f"[{self.game_id}]: Failed to send message to {curr_topic}")

			time.sleep(1)

	def close_game(self):
		"""
		This
		:return:
		"""
		for key in self.RestReceiver.get_controlled_entities():
			self.client.unsubscribe(key)
		self.ACTIVE = False

	def perform_game_start(self):
		"""

		:return:
		"""
		self.ui.frames[GameSelector].list.insert(0, *self.resource_handler.get_games())
		self.game_id = self.ui.frames[GameSelector].return_game()
		self.RestReceiver = self.generate_game()
		self.start()


	def generate_game(self):
		"""
		This function generates REST Receivers for the given game.
		:return: a REST Receiver Instance
		"""
		return RestReceiver(self.resource_handler, self.connection_handler, self.game_id)


def evaluate_relevance(msg):
	"""
	This
	:param msg:
	:return:
	"""
	if dict(msg)["type"] in RELEVANT_ACTIONS:
		return True
	return False


if __name__ == '__main__':
	MQTTPublisher(None)
