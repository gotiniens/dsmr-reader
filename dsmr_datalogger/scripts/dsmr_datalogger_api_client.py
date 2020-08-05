"""
    https://dsmr-reader.readthedocs.io/en/latest/installation/datalogger.html

    Installation:
        pip3 install pyserial==3.4 requests==2.24.0 python-decouple==3.3
"""
import datetime
import logging
import time
import re

import serial
import requests
import decouple


logger = logging.getLogger('dsmrreader')


def read_telegram(url_or_port, **serial_kwargs):  # noqa: C901
    """ Opens a serial/network connection and reads it until we have a full telegram. Yields the result """
    MAX_BYTES_PER_READ = 512
    MAX_READ_TIMEOUT = 1.0

    logger.info(
        '[%s] Opening serial connection "%s" using options: %s',
        datetime.datetime.now(),
        url_or_port,
        serial_kwargs
    )

    try:
        serial_handle = serial.serial_for_url(url=url_or_port, timeout=MAX_READ_TIMEOUT, **serial_kwargs)
    except Exception as error:
        raise RuntimeError('Failed to connect: {}', error)

    buffer = ''

    while True:
        incoming_bytes = serial_handle.read(MAX_BYTES_PER_READ)
        logger.debug('[%s] Read %d Byte(s)', datetime.datetime.now(), len(incoming_bytes))

        if not incoming_bytes:
            continue

        incoming_data = str(incoming_bytes, 'latin_1')

        # Just add data to the buffer until we detect a telegram in it.
        buffer += incoming_data

        # Should work for 99% of the telegrams read. The checksum bits are optional due to legacy meters omitting them.
        match = re.search(r'(\/[^/]+\![A-Z0-9]{0,4})', buffer, re.DOTALL)

        if not match:
            continue

        telegram = match.group(1)
        buffer = ''
        yield telegram


def _send_telegram_to_remote_dsmrreader(telegram, api_url, api_key, timeout):
    """ Registers a telegram by simply sending it to the application with a POST request. """
    logger.debug('[%s] Sending telegram to API: %s', datetime.datetime.now(), api_url)
    response = requests.post(
        api_url,
        headers={'Authorization': 'Token {}'.format(api_key)},
        data={'telegram': telegram},
        timeout=timeout,  # Prevents this script from hanging indefinitely when the server or network is unavailable.
    )

    if response.status_code != 201:
        logger.error('[%s] API error: HTTP %d - %s', datetime.datetime.now(), response.status_code, response.text)
        return

    logger.debug('[%s] API response OK: Telegram received successfully', datetime.datetime.now())


def _initialize_logging():
    logging_level = logging.INFO

    if decouple.config('DATALOGGER_DEBUG_LOGGING', default=False, cast=bool):
        logging_level = logging.DEBUG

    logger.setLevel(logging_level)
    logger.addHandler(logging.StreamHandler())


def main():  # noqa: C901
    """ Entrypoint for command line execution only. """
    _initialize_logging()
    logger.info('[%s] Starting...', datetime.datetime.now())

    # Settings.
    DATALOGGER_TIMEOUT = decouple.config('DATALOGGER_TIMEOUT', default=20, cast=float)
    DATALOGGER_SLEEP = decouple.config('DATALOGGER_SLEEP', default=0.5, cast=float)
    DATALOGGER_INPUT_METHOD = decouple.config('DATALOGGER_INPUT_METHOD')
    DATALOGGER_API_HOSTS = decouple.config('DATALOGGER_API_HOSTS', cast=decouple.Csv(post_process=tuple))
    DATALOGGER_API_KEYS = decouple.config('DATALOGGER_API_KEYS', cast=decouple.Csv(post_process=tuple))

    if not DATALOGGER_API_HOSTS or not DATALOGGER_API_KEYS:
        raise RuntimeError('API_HOSTS or API_KEYS not set')

    if len(DATALOGGER_API_HOSTS) != len(DATALOGGER_API_KEYS):
        raise RuntimeError('The number of API_HOSTS and API_KEYS given do not match each other')

    serial_kwargs = {}

    if DATALOGGER_INPUT_METHOD == 'serial':
        serial_kwargs.update(dict(
            url_or_port=decouple.config('DATALOGGER_SERIAL_PORT'),
            baudrate=decouple.config('DATALOGGER_SERIAL_BAUDRATE', cast=int),
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            xonxoff=1,
            rtscts=0,
        ))
    elif DATALOGGER_INPUT_METHOD == 'ipv4':
        serial_kwargs.update(dict(
            url_or_port='socket://{}:{}'.format(
                decouple.config('DATALOGGER_NETWORK_HOST'),
                decouple.config('DATALOGGER_NETWORK_PORT', cast=int),
            )
        ))
    else:
        raise RuntimeError('Unsupported DATALOGGER_INPUT_METHOD')

    for telegram in read_telegram(**serial_kwargs):
        logger.debug("[%s] Telegram read: \n%s", datetime.datetime.now(), telegram)

        for current_server_index in range(len(DATALOGGER_API_HOSTS)):
            current_api_host = DATALOGGER_API_HOSTS[current_server_index]
            current_api_url = '{}/api/v1/datalogger/dsmrreading'.format(current_api_host)
            current_api_key = DATALOGGER_API_KEYS[current_server_index]

            try:
                _send_telegram_to_remote_dsmrreader(
                    telegram=telegram,
                    api_url=current_api_url,
                    api_key=current_api_key,
                    timeout=DATALOGGER_TIMEOUT,
                )
            except Exception as error:
                logger.exception(error)

        time.sleep(DATALOGGER_SLEEP)


if __name__ == '__main__':  # pragma: no cover
    main()
