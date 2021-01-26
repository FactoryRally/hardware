# python3.6

import random

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
discover_topic = "discover"
topic = ""
# generate client ID with pub prefix randomly
client_id = f'client-{random.randint(0, 10000000000000)}'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def discover(client: mqtt_client):
    msg = {"topic": client_id}.__str__()
    result = client.publish(discover_topic, msg)
    result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to `{discover_topic}`")
        client.subscribe(discover_topic)
    else:
        print(f"Failed to send message to {discover_topic}")
    client.unsubscribe(discover_topic)
    client.subscribe(client_id)
    subscribe(client)


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if str(msg.payload.decode()).__contains__("topic"):
            act_payload = eval(msg.payload.decode()).get('topic')
            topic = "client"+act_payload
            client.subscribe(topic)
            print(f"subscribed to `{topic}`")
        else:
            print("new")

    client.on_message = on_message



def run():
    client = connect_mqtt()
    discover(client)
    client.loop_forever()


if __name__ == '__main__':
    run()