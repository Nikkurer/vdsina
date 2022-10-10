import ipaddress
from .common import check_response
from .Service import Service
from dataclasses import dataclass


class Server:
    """
    Class to represent server information
    Args:
        server (dict): server representation from Account class
    """
    ip_addresses = []
    endpoint = 'server'
    service = Service()

    def __init__(self, server):
        self.rights = server['can']
        self.datacenter = server['datacenter']
        self.id = server['id']
        self.name = server['name']
        self.plan = server['server-plan']
        self.status = server['status']
        self.template = server['template']
        self.fqdn = server['host']
        self._get_ips(server['ip'])
        self.resources = server['data']
        self.server_plan = server['server-plan']
        self.server_group = server['server-group']
        self.template = server['template']
        self.datacenter = server['datacenter']
        self.ssh_key = server['ssh-key']
        self.bandwidth = server['bandwidth']

    def __str__(self) -> str:
        result = f'name: {self.name}\nfqdn: {self.fqdn}\nIP addresses:\n'
        for ip in self.ip_addresses:
            for key in ip.keys():
                result = f'{result}  {key}: {ip[key]}\n'
        result = f'{result}Resources:\n'
        for key in self.resources:
            resource = self.resources[key]
            result = f'{result} {key}: {resource["value"]} {resource["for"]}\n'
        return result

    def _get_ips(self, ips_raw: list):
        """
        Fill the list of IP addresses
        Args:
            ips_raw (list):
        Returns:
            None
        """
        for ip in ips_raw:
            self.ip_addresses.append(
                {'ip': ipaddress.IPv4Network(f'{ip["ip"]}/{ip["netmask"]}', False),
                 'gateway': ip['gateway'], 'mac': ip['mac']})

    def rename(self, name: str):
        """
        Rename the server
        Args:
            name (str): New name of server
        Returns:
            None
        """
        self.service.change_object(self, 'name', name)

    def reboot(self, method: str = 'hard'):
        """
        Reboot the server
        Args:
            method (str): Should be soft or hard
        Returns:
            None
        """""
        self.service.change_object(self, 'server.reboot', method)

    def reinstall(self, hostname: str, template: str = None, ssh_key: SshKey = None):
        if not template:
            template = self.template
        if not ssh_key:
            ssh_key = self.ssh_key
        self.service.change_object(self, 'server.reinstall', {'template': template, 'ssh-key': ssh_key, 'host': hostname})


@dataclass
class SshKey:
    endpoint = 'ssh-key'
    id = None
    key = None
    name = None
    service = Service()

    def __init__(self, key):
        self.id = key['id']
        self.name = key['name']
        self.key = key['data']

    def __str__(self):
        return f'SSH public key: {self.key} {self.name}'

    def rename_key(self, name):
        self.service.change_object(self, 'name', name)

    def change_key(self, key):
        self.service.change_object(self, 'data', key)


@dataclass
class IsoImage:
    id: int
    name: str
    status: str


@dataclass
class ServerGroup:
    id: int
    name: str
    type: str
    image: str
    active: bool
    description: str
