# -*- coding: utf-8 -*-
# library imports
from paho.mqtt import client as mqtt_client
import random
import time
import threading
# Own module imports
from GUI.GameGUI import GameStartPage
from GUI.InformationDisplay import InformationDisplay
from REST.RESTClient import RestReceiver

"""
This module is publishing the latest game event which can be performed by a real robot to the MQTT broker.
"""

RELEVANT_ACTIONS = ["movement"]


class MQTTPublisher:
	"""
	This class is the MQTT Sender which pushes the current game event
	to the broker with the according topic.
	"""

	# broker address and port
	broker = 'broker.emqx.io'
	port = 1883
	# random mqtt id
	client_id = f'python-mqtt-{random.randint(0, 10000)}'
	# topics for each player
	topics = []
	# ids for each robot
	ids = []
	# general topic
	GEN_TOPIC = "general"
	SETUP = False
	ACTIVE = False
	GAME_STOP = False

	def __init__(self, gui, main, connection_handler, resource_handler, game):
		"""
		This init method initiates the client connection and starts the main
		logic of the sender.

		:param: gui: ui instance to push messages
		:param: connection_handler: connection handler instance to perform connection tasks
		:param: resource_handler: resource handler to perform ReST calls
		"""
		super().__init__()
		self.main = main
		self.client = self.connect_mqtt()
		self.connection_handler = connection_handler
		self.resource_handler = resource_handler
		self.ui = gui
		self.game = game
		self.perform_game_start()

	def run(self):
		"""
		This method starts the discover process, after that starts the client loop
		and publishing.
		"""
		self.client.loop_start()
		self.discover_and_notify()
		self.publish()

	def connect_mqtt(self):
		"""
		This method creates a connection to the MQTT Broker.

		:return: a client instance
		"""

		def on_connect(client, userdata, flags, rc):
			"""
			This method is the callback for a connection try.
			:param client: the client
			:param userdata: the submitted userdata
			:param flags: the submitted connection flags
			:param rc: the response code
			"""
			if rc == 0:
				print(f"[{self.game}]: Connected to MQTT Broker!")
			else:
				print(f"[{self.game}]: Failed to connect, return code %d\n", rc)

		client = mqtt_client.Client(self.client_id)
		client.on_connect = on_connect
		client.connect(self.broker, self.port)
		return client

	def discover_and_notify(self):
		"""
		This method handles the discovery of all clients in the
		current game and performs a mapping so each robots has its virtual id.
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
			print(msg_decoded)
			# when a message on general topic no mapping is needed
			if msg.topic == self.GEN_TOPIC:
				print(f"[{self.game}]: Received message on general: {msg_decoded}")
			else:
				# perform mapping
				if not msg_decoded.__contains__('type') and self.SETUP is False:
					print(f"[{self.game}]: Received `{msg_decoded}` from `{msg.topic}` topic")
					topic = str(eval(msg.payload.decode()))
					self.topics.append(topic[topic.rindex(':')+2:topic.__len__()])
					helper_topic = 1
					if len(self.RestReceiver.get_controlled_entities()) == len(self.topics):
						for x in self.topics:
							self.ids.append(helper_topic)
							helper_topic += 1
							print(f"[{self.game}]: {helper_topic}")
							client.publish(x, {"Your client topic is": str(helper_topic)}.__str__())
						self.SETUP = True
						self.ACTIVE = True


		self.client.subscribe("discover")
		self.client.subscribe("general")
		self.client.on_message = on_message
		# wait until all robots have connected and received topic
		time.sleep(5)
		while len(self.RestReceiver.get_controlled_entities()) != len(self.topics):
			print("Waiting for clients")
			print(self.topics)
			time.sleep(5)

	def publish(self):
		"""
		This method publishes the current message to the broker with
		the according topic if a game is currently active.
		"""
		# asks the ReST each second for a new game update
		while True and self.ACTIVE:
			resp = self.RestReceiver.get_current_message()
			if resp is not None:
				msg = resp[0]
				curr_topic = resp[1]
				# when a game winner is declared, stop the process
				if str(msg).__contains__("winner"):
					self.GAME_STOP = True
					self.ui.show_frame(self.ui.frames[GameStartPage])
					self.main.reset()
				if str(msg).__contains__("game start"):
					self.informationDisplay.update_information(dict(msg)['type'])
					self.client.publish(self.GEN_TOPIC, str(msg))
				# evaluate if message should be send or just be displayed
				if evaluate_relevance(msg) and not self.GAME_STOP:
					self.informationDisplay.update_information(display_message(dict(msg)))
					result = self.client.publish(curr_topic, str(msg))
					result: [0, 1]
					status = result[0]
					if status == 0:
						print(f"[{self.game}]: Send `{msg}` to `{curr_topic}`")
					else:
						print(f"[{self.game}]: Failed to send message to {curr_topic}")

			time.sleep(1)

	def close_game(self):
		"""
		This method unsubscribes from all current clients/topics when a game ended.
		"""
		for key in self.RestReceiver.get_controlled_entities():
			self.client.unsubscribe(key)
		self.ACTIVE = False

	def perform_game_start(self):
		"""
		This method performs a fresh start for a user selected game. It it also
		called when a game is finished and a new game was chosen.
		"""
		self.RestReceiver = self.generate_game()
		self.informationDisplay = InformationDisplay()
		self.run()

	def generate_game(self):
		"""
		This function generates REST Receivers for the given game.
		:return: a REST Receiver Instance
		"""
		return RestReceiver(self.resource_handler, self.connection_handler, self.game)


def evaluate_relevance(msg):
	"""
	This function evaluates whether the message gets transported or not aka
	if a real robot can perform it.

	:param msg: the received message to check

	:return: relevant or not
	"""
	print(dict(msg)["type"])
	if dict(msg)["type"] in RELEVANT_ACTIONS:
		return True
	return False


def display_message(msg):
	"""
	This function brings the message to a displayable form.

	:param msg: current event

	:return: event display message
	"""
	return "Movement: "+msg.get('entity')+msg.get('to').get('x')+msg.get('to').get('y')


if __name__ == '__main__':
	MQTTPublisher(None)
