from .Auth import Auth
from .common import check_response


class Account(Auth):
    def __init__(self, instance):
        self.session = instance.session
        self.api_url = instance.api_url
        self.account = 'account'
        self.balance = 'account.balance'
        self.limits = 'account.limit'
        self.server_groups = 'server-group'
        self.ssh_keys = 'ssh-key'

    def __str__(self) -> str:
        account = f'Account:\n  Created: {self.account["created"]}\n  Forecast: {self.account["forecast"]}'
        balance = f'Balance:\n  Real: {self.balance["real"]}\n  Bonus: {self.balance["bonus"]}\n  Partner: {self.balance["partner"]}'
        limits = 'Limits:'
        for key in self.limits.keys():
            value = self.limits[key]
            if isinstance(value, dict):
                substr = f'{value["now"]}/{value["max"]}'
            elif isinstance(value, list | tuple | set):
                substr = f'{str(value)}'
            limits = f'{limits}\n  {key.capitalize()}: {substr}'
        result = f'{account}\n{balance}\n{limits}'
        return result

    def get_account_info(self):
        self.account = self.get_account()
        self.balance = self.get_balance()
        self.limits = self.get_limits()

    def get_parameter(self, endpoint):
        url = f'{self.api_url}{endpoint}'
        response = self.session.get(url)
        raw_data = check_response(response)
        return raw_data

    def get_account(self) -> dict:
        url = f'{self.api_url}account'
        response = self.session.get(url)
        return check_response(response)

    def get_balance(self) -> dict:
        url = f'{self.api_url}account.balance'
        response = self.session.get(url)
        return check_response(response)

    def get_limits(self) -> dict:
        url = f'{self.api_url}account.limit'
        response = self.session.get(url)
        return check_response(response)

    def get_server_groups(self):
        url = f'{self.api_url}server-group'
        response = self.session.get(url)
        self.server_groups = check_response(response)

    def get_ssh_keys(self):
        url = f'{self.api_url}ssh-key'
        response = self.session.get(url)
        return check_response(response)

    def get_servers(self):
        url = f'{self.api_url}server'
        response = self.session.get(url)
        return check_response(response)
