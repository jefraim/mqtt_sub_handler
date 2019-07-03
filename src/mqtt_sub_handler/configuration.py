
import configparser
import json
from pathlib import Path

from mqtt_sub_handler.models import Subscription


class Configuration:
    def __init__(self, ini_file):
        file = Path(ini_file)

        if not file.exists():
            raise FileNotFoundError(ini_file + " does not exist!")

        self.ini_file = ini_file

        self.config = configparser.ConfigParser()
        self.config.read(self.ini_file)

    def get_value(self, section, name):
        try:
            return self.config[section][name]
        except KeyError:
            return None


class SubscriptionsConfiguration(Configuration):

    def get_all_topics(self) -> [(str, str)]:
        return list(map(lambda subscription: (subscription.Topic, subscription.QOS), self.get_all_subscriptions()))

    def get_all_subscriptions(self) -> [Subscription]:
        return self.section_to_subscriptions(self.config.sections())

    def get_topic_subscriptions(self, topic_name):

        return list(filter(lambda subscription: subscription.Topic == topic_name,
                           self.get_all_subscriptions()))

    def section_to_subscriptions(self, sections):
        return list(map(lambda section: Subscription(self.get_value(section, 'topic'),
                                                     self.get_value(section, 'qos'),
                                                     self.get_value(section, 'action_type'),
                                                     self.get_value(section, 'action'),
                                                     json.loads(self.get_value(section, 'parameter_fields') or '[]')),
                        sections))


class ApplicationConfiguration(Configuration):

    def get(self, name):
        return self.get_value('app', name)
