from typing import Dict, Tuple


class BaseRecord:
    name: str
    ttl: int
    r_class: str = 'IN'
    r_type: str
    data: str

    def __init__(self, name: str, ttl: int, r_type: str, data: str):
        self.name = name
        self.ttl = ttl
        if r_type in self.get_available_types().keys():
            self.r_type = r_type
        self.data = data

    def __str__(self):
        return f'{self.name} {self.ttl} {self.r_class} {self.r_type} {self.data}'

    @staticmethod
    def get_available_types() -> Dict[str, str]:
        return {
            'A': 'a host address',
            'NS': 'an authoritative name server',
            'CNAME': 'the canonical name for an alias',
            'MX': 'mail exchange',
            'TXT': 'text strings',
            'AAAA': 'IP6 Address',
            'SRV': 'Server Selection'
        }


class Record(BaseRecord):
    identifier = None

    service: str = None
    protocol: str = None

    priority: int = None
    weight: int = None
    port: int = None

    target: str

    def __init__(self, *args, **kwargs):
        super(Record, self).__init__(*args)
        self.target = kwargs['target'] if 'target' in kwargs.keys() else self.data.split()[-1]
        if self.r_type in {'NS', 'CNAME', 'MX', 'SRV'} and self.target[-1] != '.':
            self.target += '.'
        priority = 10
        if self.r_type == 'MX':
            if len(self.data) == 2:
                priority = self.parse_data_mx(self.data)[0]
            if 'priority' in kwargs.keys():
                priority = kwargs['priority']
            self.set_data_mx(priority, self.target)
        elif self.r_type == 'SRV':
            service = '_http'
            protocol = '_tcp'
            if self.name[0] == '_':
                names = self.name.split('.')
                service = names[0]
                protocol = names[1]
                self.name = '.'.join(names[2:])
            if 'service' in kwargs.keys():
                service = kwargs['service']
            if 'protocol' in kwargs.keys():
                protocol = kwargs['protocol']
            weight = 100
            port = 0
            if len(self.data.split()) == 4:
                priority, weight, port = self.parse_data_srv(self.data)[:3]
            if 'priority' in kwargs.keys():
                priority = kwargs['priority']
            if 'weight' in kwargs.keys():
                weight = kwargs['weight']
            if 'port' in kwargs.keys():
                port = kwargs['port']
            self.set_name_srv(service, protocol, self.name)
            self.set_data_srv(priority, weight, port, self.target)
        if 'identifier' in kwargs.keys():
            self.identifier = kwargs['identifier']

    def get_name(self, suffix: str = None) -> str:
        name = self.name
        if self.r_type == 'SRV':
            name = self.parse_name_srv(name)[2]
        if suffix is not None:
            name += '.' + suffix
        return name

    def set_name_srv(self, service: str, protocol: str, name: str):
        self.service = service
        self.protocol = protocol
        self.name = f'{service}.{protocol}.{name}'

    def set_data_mx(self, priority: int, mail_server: str):
        if mail_server[-1] != '.':
            mail_server += '.'
        self.priority = priority
        self.target = mail_server
        self.data = f'{priority} {mail_server}'

    def set_data_srv(self, priority: int, weight: int, port: int, server_host_name: str):
        if server_host_name[-1] != '.':
            server_host_name += '.'
        self.priority = priority
        self.weight = weight
        self.port = port
        self.target = server_host_name
        self.data = f'{priority} {weight} {port} {server_host_name}'

    @staticmethod
    def parse_name_srv(name: str) -> Tuple[str, str, str]:
        names = name.split('.')
        service = names[0]
        protocol = names[1]
        n = '.'.join(names[2:])
        return service, protocol, n

    @staticmethod
    def parse_data_mx(data: str) -> Tuple[int, str]:
        priority, mail_server = data.split()
        return int(priority), mail_server

    @staticmethod
    def parse_data_srv(data: str) -> Tuple[int, int, int, str]:
        priority, weight, port, server_host_name = data.split()
        return int(priority), int(weight), int(port), server_host_name
