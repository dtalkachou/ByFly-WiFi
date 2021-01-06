#!/usr/bin/python3
import os
import requests

from argparse import ArgumentParser
from collections.abc import Iterable
from configparser import ConfigParser

from bs4 import BeautifulSoup
from colorama import init, Style, Fore

from consts import *


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

COOKIES = {'safe': '1'}
DATA = {CSRF_TOKEN_NAME: None}

def __clr_print(style, *args, **kwargs):
    slices = [(None, 1), (1, -1)]
    if len(args) > 1:
        slices.append((-1, None))
    new_args = []
    for sl in slices:
        new_args.extend(map(str, args[sl[0]:sl[1]]))
    if isinstance(style, Iterable):
        style = ''.join(style)
    new_args[0] = style + new_args[0]
    new_args[-1] = new_args[-1] + Style.RESET_ALL
    print(*new_args, **kwargs)


def connect():
    config = ConfigParser()
    config.read(os.path.join(BASE_DIR, 'conf.ini'))

    try:
        for key in config['AUTH']:
            DATA[key.lower()] = config['AUTH'][key]
    except KeyError:
        __clr_print(Fore.RED, INVALID_CONFIG_MESSAGE)
        exit(1)

    with requests.Session() as s:
        resp = s.get(BASE_URL, cookies=COOKIES)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            csrf_token = soup.select(
                f'input[name={CSRF_TOKEN_NAME}]'
            )[0]['value']
            DATA[CSRF_TOKEN_NAME] = csrf_token
            resp = s.post(CONNECT_URL, cookies=COOKIES, data=DATA)
            __clr_print(Fore.GREEN, CONNECTED_MESSAGE)
            # todo: handler alert messages
        else:
            __clr_print(Fore.RED, resp.reason)


def disconnect():
    resp = requests.post(DISCONNECT_URL)
    __clr_print(Fore.YELLOW, DISCONNECTED_MESSAGE)


def main():
    # Init colorama on Windows
    init()

    parser = ArgumentParser(description=ARGUMENT_PARSER_DESCRIPRION)
    parser.add_argument('action', choices=ARGUMENT_PARSER_ACTION_CHOICES,
                        default=ARGUMENT_PARSER_ACTION_CHOICES[0],
                        help=ARGUMENT_PARSER_ACTION_HELP)
    args = parser.parse_args()

    try:
        if args.action in ARGUMENT_PARSER_ACTION_CONNECT_CHOICES:
            connect()
        else:
            disconnect()
    except requests.exceptions.ConnectionError as err:
        __clr_print(Fore.RED, err)
    

if __name__ == '__main__':
    main()
