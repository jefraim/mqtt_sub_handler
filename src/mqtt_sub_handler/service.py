import logging

from mqtt_sub_handler.mqtt import Connection
from mqtt_sub_handler.configuration import ApplicationConfiguration


def main():
    app_config = ApplicationConfiguration('/etc/mqtt_sub_handler/config.ini')
    logging.basicConfig(filename=app_config.get_value('app', 'log_file'), level=logging.DEBUG,
                        format='%(asctime)-15s %(message)s')

    logging.debug('Starting up ...')

    connection = Connection()
    logging.debug('Connecting ...')
    connection.connect()

    logging.debug('Listening ...')
    connection.listen()

    logging.debug('Stopping ...')


if __name__ == '__main__':
    main()
