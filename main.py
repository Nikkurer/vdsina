import argparse
from vdsina.Server import Server
from vdsina.Account import Account

API_URL = 'https://userapi.vdsina.ru/v1/'


def get_arguments():
    arg_parser = argparse.ArgumentParser(add_help=True, description='https://vdsina.ru API interaction')
    arg_parser.add_argument('--get-token', '-t', action='store_true', required=False, dest='token',
                            help='Get token with login and password auth')
    return arg_parser.parse_args()


if __name__ == '__main__':
    servers = []
    account = Account(API_URL)
    print(account)
    print(f'Servers:')
    for server in account.servers:
        servers.append(Server(server))
    for server in servers:
        print(server)

