import json
import os
import ipaddress


class Server:
    def __init__(self, server):
        self.rights = server['can']
        self.datacenter = server['datacenter']
        self.fullname = server['full_name']
        self.id = server['id']
        self.name = server['name']
        self.plan = server['server-plan']
        self.status = server['status']
        self.template = server['template']
        self.ipaddress = str(ipaddress.IPv4Network(f'{server["ip"]["ip"]}/{server["ip"]["netmask"]}', False))
        self.fqdn = server['ip']['host']
        self.gateway = server['ip']['gateway']

    def __str__(self) -> str:
        result = f'name: {self.name}\nip: {self.ipaddress}\nfqdn: {self.fqdn}'
        return result
