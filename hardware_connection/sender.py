from paho.mqtt import client as mqtt_client
import random
from REST_Client import RestReceiver

broker = 'broker.emqx.io'
port = 1883
client_id = f'python-mqtt-{random.randint(0, 10000000000000)}'
topics = []
ids = []

input_msg = measurement = {
	"clients": 2,
}


def connect_mqtt():
	def on_connect(client, userdata, flags, rc):
		if rc == 0:
			print("Connected to MQTT Broker!")
		else:
			print("Failed to connect, return code %d\n", rc)

	client = mqtt_client.Client(client_id)
	client.on_connect = on_connect
	client.connect(broker, port)
	return client


discover_topic = "discover"


def discover_and_notify(client):
	def on_message(client, userdata, msg):
		# client.publish(client_id,msg.topic)
		print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
		topics.append(eval(msg.payload.decode()).get("topic"))
		helper_topic = 1
		# for x in topics: print("topics" + x)
		print("length " + str(len(topics)))
		if input_msg.get("clients") == len(topics):
			for x in topics:
				ids.append(helper_topic)
				helper_topic += 1
				# print(helper_topic)
				client.publish(x, {"topic": str(helper_topic)}.__str__())
				print("HERE IS X " + x)

	client.subscribe(discover_topic)
	client.on_message = on_message


def publish(client):
	msg = {"topic": "topic"}.__str__()
	result = client.publish(discover_topic, msg)
	result: [0, 1]
	status = result[0]
	if status == 0:
		print(f"Send `{msg}` to `{discover_topic}`")
		client.subscribe(discover_topic)
	else:
		print(f"Failed to send message to {discover_topic}")


def run():
	client = connect_mqtt()
	discover_and_notify(client)
	# publish(client)
	client.loop_forever()


if __name__ == '__main__':
	RestReceiver()
	run()

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
