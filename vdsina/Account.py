import json

from .Auth import Auth
from .common import check_response
from email_validator import validate_email, EmailNotValidError


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
        self.templates = self.get_parameter('template')
        self.datacenters = self.get_parameter('datacenter')
        self.limits = self.get_parameter('account.limit')
        self.balance = self.get_parameter('account.balance')
        self.server_groups = self.get_parameter('server-group')
        self.get_ssh_keys()
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

    def get_parameter(self, endpoint, parameter_id=None):
        """Get parameter by its endpoint"""
        url = f'{self.api_url}{endpoint}'
        if parameter_id:
            url = f'{url}/{parameter_id}'
        response = self.session.get(url)
        return check_response(response)

    def get_sever_plans(self, sg_id):
        url = f'{self.api_url}server-plan/{sg_id}'
        response = self.session.get(url)
        self.server_plans[sg_id] = check_response(response)

    def create_user(self, email: str):
        url = f'{self.api_url}register'
        # TODO: add partner code support
        try:
            validation = validate_email(email, check_deliverability=False)
            email = validation.email
            payload = json.dumps({"email": email})
            response = self.session.post(url, data=payload)
            return check_response(response)
        except EmailNotValidError as e:
            return str(e)

    def get_ssh_keys(self):
        self.ssh_keys = []
        ssh_keys = self.get_parameter('ssh-key')
        for ssh_key in ssh_keys:
            self.ssh_keys.append(self.get_parameter('ssh-key', ssh_key['id']))
