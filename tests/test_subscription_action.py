import  pytest

from mqtt_sub_handler.action import CommandFormatter, ActionFactory
from mqtt_sub_handler.models import Subscription


def test_action_command_formatter_1():
    formatter = CommandFormatter(
        Subscription('test/topic', '0', 'command', 'gammu-smsd-inject TEXT {} -text "{}"', ['from', 'message'])
    )

    command = formatter.format('{"from":"+639085329898","message":"this is a test message"}')

    assert command == 'gammu-smsd-inject TEXT +639085329898 -text "this is a test message"'


def test_action_command_formatter_2():
    formatter = CommandFormatter(
        Subscription('test/topic', '0', 'command', 'app-command {0} -param1 {1} -param2 {1}', ['val0', 'val1'])
    )

    command = formatter.format('{"val0":"yes","val1":"yes yes"}')

    assert command == 'app-command yes -param1 yes yes -param2 yes yes'


def test_action_command_formatter_3():
    formatter = CommandFormatter(
        Subscription('test/topic', '0', 'command', 'app-command {0} -param1 {1} -param2 {1}', ['val0', 'val1'])
    )

    with pytest.raises(Exception) as e:
        formatter.format('{"val0":"yes"}')

    assert str(e.value) == "Required parameter=''val1'' data was not found."


def test_action_command_1():
    subscription = Subscription('test/topic', '0', 'command', 'echo {}', ['val0'])

    action = ActionFactory.get(subscription)

    result = action.do('{"val0":"yes"}')

    assert result == "b'yes\\n'"


def test_action_command_with_error():
    subscription = Subscription('test/topic', '0', 'command', 'echo {}-{}', ['val0', 'val1'])

    action = ActionFactory.get(subscription)

    result = action.do('{"val0":"yes"}')

    assert result == "Failed to execute 'echo {}-{}' with result=Required parameter=''val1'' data was not found."


def test_action_factory_unknown_action():
    subscription = Subscription('test/topic', '0', 'unknown_action', 'echo {}', ['val0'])

    with pytest.raises(Exception) as e:
        ActionFactory.get(subscription)

    assert str(e.value) == "Unknown action type: unknown_action"
