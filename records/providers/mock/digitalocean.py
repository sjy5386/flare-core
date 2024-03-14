import responses


class MockDigitalOceanDnsRecord:
    host = 'https://api.digitalocean.com'

    def __init__(self):
        self.list_all_domain_records()
        self.create_a_new_domain_record()
        self.retrieve_an_existing_domain_record()
        self.update_a_domain_record()
        self.delete_a_domain_record()

    def list_all_domain_records(self):
        responses.get(
            self.host + '/v2/domains/example.com/records',
            json={
                'domain_records': [
                    {
                        'id': 28448429,
                        'type': 'NS',
                        'name': '@',
                        'data': 'ns1.digitalocean.com',
                        'priority': None,
                        'port': None,
                        'ttl': 1800,
                        'weight': None,
                        'flags': None,
                        'tag': None,
                    },
                    {
                        'id': 28448430,
                        'type': 'NS',
                        'name': '@',
                        'data': 'ns2.digitalocean.com',
                        'priority': None,
                        'port': None,
                        'ttl': 1800,
                        'weight': None,
                        'flags': None,
                        'tag': None,
                    },
                    {
                        'id': 28448431,
                        'type': 'NS',
                        'name': '@',
                        'data': 'ns3.digitalocean.com',
                        'priority': None,
                        'port': None,
                        'ttl': 1800,
                        'weight': None,
                        'flags': None,
                        'tag': None,
                    },
                    {
                        'id': 28448432,
                        'type': 'A',
                        'name': 'test',
                        'data': '1.2.3.4',
                        'priority': None,
                        'port': None,
                        'ttl': 1800,
                        'weight': None,
                        'flags': None,
                        'tag': None,
                    }
                ],
                'links': {
                },
                'meta': {
                    'total': 4,
                }
            }
        )

    def create_a_new_domain_record(self):
        responses.post(
            self.host + '/v2/domains/example.com/records',
            json={
                'domain_record': {
                    'id': 28448433,
                    'type': 'A',
                    'name': 'www',
                    'data': '162.10.66.0',
                    'priority': None,
                    'port': None,
                    'ttl': 1800,
                    'weight': None,
                    'flags': None,
                    'tag': None,
                }
            },
            status=201,
        )

    def retrieve_an_existing_domain_record(self):
        responses.get(
            self.host + '/v2/domains/example.com/records/3352896',
            json={
                'domain_record': {
                    'id': 3352896,
                    'type': 'A',
                    'name': 'blog',
                    'data': '162.10.66.0',
                    'priority': None,
                    'port': None,
                    'ttl': 1800,
                    'weight': None,
                    'flags': None,
                    'tag': None,
                }
            }
        )

    def update_a_domain_record(self):
        responses.put(
            self.host + '/v2/domains/example.com/records/3352896',
            json={
                'domain_record': {
                    'id': 3352896,
                    'type': 'A',
                    'name': 'blog',
                    'data': '162.10.66.0',
                    'priority': None,
                    'port': None,
                    'ttl': 1800,
                    'weight': None,
                    'flags': None,
                    'tag': None,
                }
            }
        )

    def delete_a_domain_record(self):
        responses.delete(
            self.host + '/v2/domains/example.com/records/3352896',
            status=204,
        )
