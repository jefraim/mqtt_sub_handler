import paho.mqtt.client as mqtt
import logging

from mqtt_sub_handler.configuration import SubscriptionsConfiguration
from mqtt_sub_handler.action import ActionFactory

# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        subscriptions = SubscriptionsConfiguration('/etc/mqtt_sub_handler/subscriptions.ini')
        client.client.subscribe(subscriptions.get_all_topics())
    else:
        logging.debug("Failed to connect to the MQTT broker")

# The callback for when a PUBLISH message is received from the server.


def on_subscribe(client, userdata, mid, granted_qos):

    logging.debug("on_subscribe callback result="+str(mid) + ", granted_qos"+str(granted_qos))


def on_message(client, userdata, msg):
    logging.debug("Processing: " + msg.topic + " " + str(msg.payload))
    subscriptions_config = SubscriptionsConfiguration('/etc/mqtt_sub_handler/subscriptions.ini')
    subscriptions = subscriptions_config.get_topic_subscriptions(msg.topic)

    for subscription in subscriptions:
        action = ActionFactory.get(subscription)
        result = action.do(str(msg.payload))
        client.publish(subscription.Topic, "result: ".format(result))

    logging.debug("Processing Done for " + msg.topic)


def on_disconnect(client, userdata, rc):
    logging.debug("Disconnected from MQTT broker!")


class Connection:
    def __init__(self):
        self.client = mqtt.Client()

    def connect(self, host, port, keep_alive):
        self.client.on_message = on_message
        self.client.on_connect = on_connect
        self.client.on_disconnect = on_disconnect

        self.client.connect(host, port, keep_alive)

    def listen(self):
        self.client.loop_forever()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

