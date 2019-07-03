import subprocess
import logging
import json
import shlex


class CommandFormatter:
    def __init__(self, subscription):
        self.subscription = subscription

    def format(self, data):
        json_data = json.loads(data)

        try:
            parameter_values = list(map(lambda field: json_data[field], self.subscription.ParameterFields))
        except KeyError as e:
            raise Exception("Required parameter='{}' data was not found.".format(e))

        return str(self.subscription.Action).format(*parameter_values)


class CommandAction:
    def __init__(self, subscription):
        self.subscription = subscription

    def do(self, data):
        try:
            command = CommandFormatter(self.subscription).format(data)
            res = str(subprocess.run(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout)

        except Exception as e:
            res = "Failed to execute '%s' with result=%s" % (str(self.subscription.Action), str(e))

        logging.debug('CommandAction Do result=' + res)
        return res


class ActionFactory:
    @staticmethod
    def get(subscription):
        if subscription.ActionType == 'command':
            return CommandAction(subscription)
        else:
            raise Exception('Unknown action type: ' + subscription.ActionType)
