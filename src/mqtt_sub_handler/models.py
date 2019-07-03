class Subscription:
    def __init__(self, topic, qos, action_type, action, parameter_fields):
        self.Topic = topic
        self.QOS = qos
        self.ActionType = action_type
        self.Action = action
        self.ParameterFields = parameter_fields
