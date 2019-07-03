import pytest

from mqtt_sub_handler.configuration import SubscriptionsConfiguration, ApplicationConfiguration


def test_get_but_subscription_file_does_not_exist():
    with pytest.raises(FileNotFoundError):
        SubscriptionsConfiguration('subscriptions_not_exist.ini')


def test_subscriptions_get_all_subscriptions():
    subscriptions = SubscriptionsConfiguration('./tests/subscriptions.ini')
    data = subscriptions.get_all_subscriptions()

    assert len(data) == 3
    assert data[0].Topic == 'topic/test/one'
    assert data[0].QOS == '0'
    assert data[0].ActionType == 'command'
    assert data[0].Action == 'gammu-smsd-inject TEXT 123456 -text "All your base are belong to us one"'
    assert len(data[0].ParameterFields) == 0
    assert data[1].Topic == 'topic/test/two'
    assert data[1].QOS == '1'
    assert data[1].ActionType == 'command'
    assert data[1].Action == 'gammu-smsd-inject TEXT 123456 -text "All your base are belong to us two"'
    assert len(data[1].ParameterFields) == 0
    assert data[2].Topic == 'topic/test/three'
    assert data[2].QOS == '2'
    assert data[2].ActionType == 'command'
    assert data[2].Action == 'gammu-smsd-inject TEXT {} -text "{}"'
    assert len(data[2].ParameterFields) == 2
    assert data[2].ParameterFields[0] == "from"
    assert data[2].ParameterFields[1] == "message"


def test_subscriptions_get_all_topics():
    subscriptions = SubscriptionsConfiguration('./tests/subscriptions.ini')
    data = subscriptions.get_all_topics()

    assert len(data) == 3
    assert data[0][0] == 'topic/test/one'
    assert data[0][1] == '0'
    assert data[1][0] == 'topic/test/two'
    assert data[1][1] == '1'
    assert data[2][0] == 'topic/test/three'
    assert data[2][1] == '2'


def test_get_topic_subscriptions():
    subscriptions = SubscriptionsConfiguration('./tests/subscriptions.ini')
    data = subscriptions.get_topic_subscriptions('topic/test/one')

    assert len(data) == 1
    assert data[0].Topic == 'topic/test/one'
    assert data[0].QOS == '0'
    assert data[0].ActionType == 'command'
    assert data[0].Action == 'gammu-smsd-inject TEXT 123456 -text "All your base are belong to us one"'


def test_subscriptions_get_all_subscriptions():
    subscriptions = SubscriptionsConfiguration('./tests/subscriptions2.ini')
    data = subscriptions.get_topic_subscriptions('topic/test/one')

    assert len(data) == 2
    assert data[0].Topic == 'topic/test/one'
    assert data[0].QOS == '0'
    assert data[0].ActionType == 'command'
    assert data[0].Action == 'gammu-smsd-inject TEXT 123456 -text "All your base are belong to us one"'
    assert data[1].Topic == 'topic/test/one'
    assert data[1].QOS == '1'
    assert data[1].ActionType == 'command'
    assert data[1].Action == 'gammu-smsd-inject TEXT 123456 -text "All your base are belong to us two"'


def test_app_get():
    app = ApplicationConfiguration('tests/config.ini')
    assert app.get('mqtt_host') == 'localhost'

# if __name__ == '__main__':
#     unittest.main()
