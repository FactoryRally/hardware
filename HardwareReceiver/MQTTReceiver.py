import random as rd
from paho.mqtt import client as MQTTClient

"""
This module is an example and non functional implementation of a "real" robot.
"""


def execute_command(msg, event_type):
    """
    This method executes the received command and currently only is reacting to a MovementEvent.

    :param: msg: the decoded message containing game info
    :param: event_type: the given event type
    """
    msg_decoded = dict(msg)
    if event_type == "movement":
        print(f"perform_movement({msg_decoded.get('entity')}, {msg_decoded.get('direction')}, "
              f"{msg_decoded.get('rotation')}, {msg_decoded.get('rotation-times')}, {msg_decoded.get('to').get('x')},"
              f" {msg_decoded.get('to').get('y')}")


class MQTTReceiver:
    """
    This class is an example implementation of a MQTT Receiver which
    receives and handles the transmitted data.
    """

    broker = 'broker.emqx.io'
    port = 1883
    discover_topic = "discover"
    topic = ""
    general_topic = "general"
    # generate client ID with pub prefix randomly
    client_id = f'client-{rd.randint(0, 10000)}'
    id_received = False

    def __init__(self):
        """
        This init function initiates the connection to the MQTT broker and
        starts the transmission.
        """
        self.client = self.connect_mqtt()
        self.discover()
        self.subscribe()
        self.client.loop_forever()

    def connect_mqtt(self):
        """
        This function creates a connection to the MQTT Broker.

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

        client = MQTTClient.Client(self.client_id)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def discover(self):
        """
        This function is used for the discovery phase on the start of the game, so each robot gets his virtual id.
        """
        msg = {"This client topic is": self.client_id}.__str__()
        result = self.client.publish(self.discover_topic, msg)
        result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to `{self.discover_topic}`")
            self.client.subscribe(self.discover_topic)
        else:
            print(f"Failed to send message to {self.discover_topic}")
        self.client.unsubscribe(self.discover_topic)
        self.client.subscribe(self.general_topic)
        print(self.client_id)
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
            :param client: the client instance
            :param userdata: the submitted userdata
            :param msg: the transmitted message
            """
            msg_decoded = msg.payload.decode()
            if self.id_received:
                execute_command(msg_decoded)
            elif not self.id_received and str(msg_decoded).__contains__("Your client topic is"):
                act_payload = eval(msg.payload.decode()).get('topic')
                self.topic = "client-"+act_payload
                client.subscribe(self.topic)
                print(f"subscribed to `{self.topic}`")
                self.id_received = True
            else:
                print(msg_decoded)

        self.client.on_message = on_message
        if not self.id_received:
            print("GAME PHASE not started!")


if __name__ == '__main__':
    MQTTReceiver()
