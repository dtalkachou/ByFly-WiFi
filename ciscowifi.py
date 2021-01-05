#!/usr/bin/python3
from requests import Session
from collections.abc import Iterable
from configparser import ConfigParser

from bs4 import BeautifulSoup

from consts import (
    BASE_URL,
    CONNECT_URL,
    CSRF_TOKEN_NAME,
    CONNECTED_MESSAGE,
    INVALID_CONFIG_MESSAGE,
)

from colorama import Style, Fore

COOKIES = {'safe': '1'}
DATA = {CSRF_TOKEN_NAME: None}


def clr_print(style, *args, **kwargs):
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


def main():
    config = ConfigParser()
    config.read('conf.ini')

    try:
        for key in config['AUTH']:
            DATA[key.lower()] = config['AUTH'][key]
    except KeyError:
        clr_print(Fore.RED, INVALID_CONFIG_MESSAGE)
        exit(1)


    with Session() as s:
        resp = s.get(BASE_URL, cookies=COOKIES)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            csrf_token = soup.select(
                f'input[name={CSRF_TOKEN_NAME}]'
            )[0]['value']
            DATA[CSRF_TOKEN_NAME] = csrf_token
            resp = s.post(CONNECT_URL, cookies=COOKIES, data=DATA)
            clr_print(Fore.GREEN, CONNECTED_MESSAGE)
            # todo: handler alert messages
        else:
            clr_print(Fore.RED, resp.reason)


if __name__ == '__main__':
    main()
