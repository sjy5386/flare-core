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
