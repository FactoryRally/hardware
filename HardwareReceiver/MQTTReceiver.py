import random
from paho.mqtt import client as mqtt_client


class MQTTReceiver:
    """
    This class is an example implementation of a MQTT Receiver which
    receives and handles the transmitted data.
    """

    broker = 'broker.emqx.io'
    port = 1883
    discover_topic = "discover"
    topic = "general"
    # generate client ID with pub prefix randomly
    client_id = f'client-{random.randint(0, 10000)}'

    def __init__(self):
        """
        This init function initiates the connection to the MQTT broker and
        starts the transmission.
        """
        self.client = self.connect_mqtt()
        self.discover()
        self.subscribe()
        self.client.loop_forever()

    def connect_mqtt(self) -> mqtt_client:
        """
        This function creates a client connection to the MQTT Broker.
        :return: a client instance
        """

        def on_connect(client, userdata, flags, rc):
            """
            This function is the callback for a connection.
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

    def discover(self):
        """
        This function is used for the discovery phase on the start of the game.
        """
        msg = {"topic": self.client_id}.__str__()
        result = self.client.publish(self.discover_topic, msg)
        result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to `{self.discover_topic}`")
            self.client.subscribe(self.discover_topic)
        else:
            print(f"Failed to send message to {self.discover_topic}")
        self.client.unsubscribe(self.discover_topic)
        self.client.subscribe(self.client_id)

    def subscribe(self):
        """
        This function handles the main logic of the receiver and
        prints out the according event for the robot.
        """

        def on_message(client, userdata, msg):
            """
            This function is the callback which gets called when a
            message is received.
            :param client: the client connection
            :param userdata:
            :param msg:
            """
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            if str(msg.payload.decode()).__contains__("topic"):
                act_payload = eval(msg.payload.decode()).get('topic')
                topic = "client"+act_payload
                client.subscribe(topic)
                print(f"subscribed to `{topic}`")
            else:
                print("Message is currently unacceptable!")

        self.client.on_message = on_message


if __name__ == '__main__':
    MQTTReceiver()
