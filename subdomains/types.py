from typing import Tuple


class Record:
    name: str
    ttl: int
    record_class: str = 'IN'
    record_type: str
    data: str

    def __init__(self, name: str, ttl: int, record_type: str, data: str):
        self.name = name
        self.ttl = ttl
        self.record_type = record_type
        self.data = data

    def __str__(self):
        return f'{self.name} {self.ttl} {self.record_class} {self.record_type} {self.data}'


class ARecord(Record):  # a host address
    def __init__(self, name: str, ttl: int, ip_address: str):
        super().__init__(name, ttl, 'A', ip_address)


class NsRecord(Record):  # an authoritative name server
    def __init__(self, name: str, ttl: int, name_server: str):
        super().__init__(name, ttl, 'NS', name_server)


class CnameRecord(Record):  # the canonical name for an alias
    def __init__(self, name: str, ttl: int, alias: str):
        super().__init__(name, ttl, 'CNAME', alias)


class MxRecord(Record):  # mail exchange
    def __init__(self, name: str, ttl: int, mail_server: str, priority: int):
        super().__init__(name, ttl, 'MX', f'{priority} {mail_server}')
        self.mail_server = mail_server
        self.priority = priority

    def get_data(self) -> Tuple[str, str]:
        priority, mail_server = self.data.split(' ')
        return mail_server, priority

    def set_data(self, mail_server: str, priority: int):
        self.data = f'{priority} {mail_server}'


class TxtRecord(Record):  # text strings
    def __init__(self, name: str, ttl: int, value: str):
        super().__init__(name, ttl, 'TXT', value)


class AaaaRecord(ARecord):  # IP6 Address
    def __init__(self, name: str, ttl: int, ip_address: str):
        super().__init__(name, ttl, ip_address)
        self.record_type = 'AAAA'
