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

    while True:
        action = input('What do you want to do? ((S)how|(A)dd|(D)elete|(E)xit ')
        if action in ('Show', 'S'):
            for ssh_key in account.ssh_keys:
                print(ssh_key)
        elif action in ('Add', 'A'):
            ssh_key_name = input('Enter ssh key name: ')
            ssh_key_fingerprint = input('Enter public ssh key: ')
            account.add_ssh_key(ssh_key_name, ssh_key_fingerprint)
        elif action in ('Delete', 'D'):
            ssh_key_id = input('Which key you want to delete? (id) ')
            account.delete_ssh_key(int(ssh_key_id))
        else:
            break


