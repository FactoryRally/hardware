from paho.mqtt import client as mqtt_client
import random
from threading import Thread
import time


class MQTTSender(Thread):
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
		print("DONE")
		#self.player_id = player_id

	def run(self):
		"""

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
				print("Connected to MQTT Broker!")
			else:
				print("Failed to connect, return code %d\n", rc)

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
			# client.publish(client_id,msg.topic)
			print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
			if not str(msg.payload.decode()).__contains__('type'):
				self.topics.append(eval(msg.payload.decode())[2])
				helper_topic = 1
				# for x in topics: print("topics" + x)
				print("length " + str(len(self.topics)))
				if self.RestReceiver.get_controlled_entities() == len(self.topics):
					for x in self.topics:
						self.ids.append(helper_topic)
						helper_topic += 1
						# print(helper_topic)
						client.publish(x, {"topic": str(helper_topic)}.__str__())
						print("HERE IS X " + x)

		self.client.subscribe(self.discover_topic)
		self.client.on_message = on_message

	def publish(self):
		"""
		This method publishes the current message to the broker with
		the according topic.
		:return:
		"""
		while True:
			resp = self.RestReceiver.get_current_message()
			if resp is not None:
				print(resp)
				msg = resp[0]
				curr_topic = resp[1]
				result = self.client.publish(curr_topic, str(msg))
				result: [0, 1]
				status = result[0]
				if status == 0:
					print(f"Send `{msg}` to `{curr_topic}`")
				else:
					print(f"Failed to send message to {curr_topic}")

			time.sleep(1)


if __name__ == '__main__':
	MQTTSender(None)

#  for x in range(input_msg.get("number_of_clients")):
#      msg = {f"discover @ client":f"`{x}`", "with topic":f"`{x}`"}.__str__()
#      topic = f"client {x}"

#      result = client.publish(discover_topic, msg)
#     result: [0, 1]
##     status = result[0]
#    if status == 0:
#        print(f"Send `{msg}` to `{topic}`")
#   else:
#      print(f"Failed to send message to {topic}")
#  topics.append(topic)
