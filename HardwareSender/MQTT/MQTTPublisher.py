import json
from paho.mqtt import client as mqtt_client
import random
from threading import Thread
import time


class MQTTPublisher():
	"""
	This class is the MQTT Sender which pushes the current game event
	to the broker on the according topic.
	"""

	broker = 'broker.emqx.io'
	port = 1883
	client_id = f'python-mqtt-{random.randint(0, 10000)}'
	topics = []
	ids = []
	discover_topic = "general"

	def __init__(self, rest_receiver):
		"""
		This init method initiates the client connection and starts the main
		logic of the sender.
		"""
		self.client = self.connect_mqtt()
		self.RestReceiver = rest_receiver
		self.game_id = self.RestReceiver.game_id

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

			if not str(msg.payload.decode()).__contains__('type'):
				print(f"[{self.game_id}]: Received `{msg.payload.decode()}` from `{msg.topic}` topic")
				self.topics.append(eval(msg.payload.decode())[2])
				helper_topic = 1
				if self.RestReceiver.get_controlled_entities() == len(self.topics):
					for x in self.topics:
						self.ids.append(helper_topic)
						helper_topic += 1
						print(f"[{self.game_id}]: {helper_topic}")
						client.publish(x, {"Your client topic is": str(helper_topic)}.__str__())
			if msg.topic == "general":
				print(f"[{self.game_id}]: Received message on general: {msg.payload.decode()}")

		self.client.subscribe(self.discover_topic)
		self.client.on_message = on_message
		while self.RestReceiver.get_controlled_entities() != len(self.topics):
			continue

	def publish(self):
		"""
		This method publishes the current message to the broker with
		the according topic.
		"""
		while True:
			resp = self.RestReceiver.get_current_message()
			obj = json.dumps(resp)
			print(obj)
			if resp is not None:
				msg = resp[0]
				curr_topic = resp[1]
				result = self.client.publish(curr_topic, str(msg))
				result: [0, 1]
				status = result[0]
				if status == 0:
					print(f"[{self.game_id}]: Send `{msg}` to `{curr_topic}`")
				else:
					print(f"[{self.game_id}]: Failed to send message to {curr_topic}")

			time.sleep(1)


if __name__ == '__main__':
	MQTTPublisher(None)
