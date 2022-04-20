import argparse
import os
import requests
from Vdsina import Account, Server

API_URL = 'https://userapi.vdsina.ru/v1/'
LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
TOKEN = os.getenv('TOKEN')


def get_arguments():
    arg_parser = argparse.ArgumentParser(add_help=True, description='https://vdsina.ru API interaction')
    arg_parser.add_argument('--get-token', '-t', action='store_true', required=False, dest='token',
                            help='Get token with login and password auth')
    return arg_parser.parse_args()


if __name__ == '__main__':
    session = requests.Session()
    session.headers.update({'Content-Type': 'application/json'})
    instance = Account(session, API_URL)
    session.headers.update({'Authorization': instance.check_auth()})
    servers = []
    for server in instance.get_servers():
        servers.append(Server(server))
    for server in servers:
        print(server)

