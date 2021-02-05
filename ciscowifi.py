#!/usr/bin/python3
import os
import re

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


def config_to_data(section):
    config = ConfigParser()
    config.read(os.path.join(BASE_DIR, 'conf.ini'))

    try:
        for key in config[section]:
            DATA[key.lower()] = config[section][key]
    except KeyError:
        __clr_print(Fore.RED, INVALID_CONFIG_MESSAGE)
        exit(1)


def connect(s):
    config_to_data('AUTH')
    resp = s.post(CONNECT_URL, cookies=COOKIES, data=DATA)
    soup = BeautifulSoup(resp.content, 'html.parser')
    first_child = soup.find('div', class_='form').find()

    if first_child.name == 'h3':
        __clr_print(Fore.GREEN, first_child.find(text=True))
    else:
        cookies_dict = s.cookies.get_dict()
        if MESSAGES_COOKIE_NAME not in cookies_dict:
            __clr_print(Fore.YELLOW, UNKNOWN_BEHAVIOR_MESSAGE)
            return
        messages = re.sub(
            r'\\{2}',
            r'\\',
            cookies_dict[MESSAGES_COOKIE_NAME]
        ).encode().decode('unicode_escape')
        msg_text = re.findall(r'\[.*,(.*?)\]', messages)[0]
        __clr_print(Fore.RED, msg_text)


def disconnect(s):
    resp = s.post(DISCONNECT_URL, data=DATA)
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
        with requests.Session() as s:
            s.cookies.update(COOKIES)

            resp = s.get(BASE_URL)
            if resp.status_code == 200:
                csrf_token = BeautifulSoup(resp.content, 'html.parser') \
                    .select(f'input[name={CSRF_TOKEN_NAME}]')[0]['value']
                DATA[CSRF_TOKEN_NAME] = csrf_token
                if args.action in ARGUMENT_PARSER_ACTION_CONNECT_CHOICES:
                    connect(s)
                else:
                    disconnect(s)
            else:
                __clr_print(Fore.RED, resp.reason)
    except requests.exceptions.ConnectionError as err:
        __clr_print(Fore.RED, err)
    

if __name__ == '__main__':
    main()
