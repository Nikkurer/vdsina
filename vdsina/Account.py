import json

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
    servers = None
    ssh_keys = []
    templates = None
    datacenters = None
    server_groups = None
    server_plans = {}

    def __init__(self, api_url: str):
        """Inits Account with api_url (str) as provider API server URL"""
        super().__init__(api_url)
        self.account = self.get_parameter('account')
        self.servers = self.get_parameter('server')
        self.ssh_keys = self.get_parameter('ssh-key')
        self.templates = self.get_parameter('template')
        self.datacenters = self.get_parameter('datacenter')
        self.limits = self.get_parameter('account.limit')
        self.balance = self.get_parameter('account.balance')
        self.server_groups = self.get_parameter('server-group')

        for server_group in self.server_groups:
            self.get_sever_plans(server_group['id'])

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

    def get_parameter(self, endpoint):
        """Get parameter by its endpoint"""
        url = f'{self.api_url}{endpoint}'
        response = self.session.get(url)
        return check_response(response)

    def get_sever_plans(self, sg_id):
        url = f'{self.api_url}server-plan/{sg_id}'
        response = self.session.get(url)
        self.server_plans[sg_id] = check_response(response)

    def create_user(self, email):
        url = f'{self.api_url}register'
        # TODO: add partner code support
        payload = json.dumps({"email": email})
        response = self.session.post(url, data=payload)
        return check_response(response)