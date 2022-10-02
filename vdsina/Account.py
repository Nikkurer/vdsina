from .Auth import Auth
from .common import check_response


class Account(Auth):
    """VDSina account info

    The class for getting information about VDSina account and do some operations with it

    Args:
         api_url (str): Provider API server URL

    Attributes:
        account (dict): Account info
        limits (dict): Account limits
        balance (dict): Account balance
        server_groups (list): Account available server groups
    """
    limits = None
    balance = None
    account = None
    server_groups = None

    def __init__(self, instance, api_url):
        super().__init__(api_url)
        self.session = instance.session
        self.api_url = instance.api_url

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
            else:
                raise TypeError()
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
