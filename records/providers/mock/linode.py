import responses


class MockLinodeDnsRecord:
    host = 'https://api.linode.com'

    def __init__(self):
        self.domains_list()
        self.domain_records_list()
        self.domain_record_create()
        self.domain_record_delete()
        self.domain_record_view()
        self.domain_record_update()

    def domains_list(self):
        responses.get(
            self.host + '/v4/domains',
            json={
                'data': [
                    {
                        'axfr_ips': [],
                        'description': None,
                        'domain': 'example.org',
                        'expire_sec': 300,
                        'group': None,
                        'id': 1234,
                        'master_ips': [],
                        'refresh_sec': 300,
                        'retry_sec': 300,
                        'soa_email': 'admin@example.org',
                        'status': 'active',
                        'tags': [
                            'example tag',
                            'another example'
                        ],
                        'ttl_sec': 300,
                        'type': 'master'
                    }
                ],
                'page': 1,
                'pages': 1,
                'results': 1,
            },
        )

    def domain_records_list(self):
        responses.get(
            self.host + '/v4/domains/1234/records',
            json={
                'data': [
                    {
                        'created': '2018-01-01T00:01:01',
                        'id': 123456,
                        'name': 'test',
                        'port': 80,
                        'priority': 50,
                        'protocol': None,
                        'service': None,
                        'tag': None,
                        'target': '192.0.2.0',
                        'ttl_sec': 604800,
                        'type': 'A',
                        'updated': '2018-01-01T00:01:01',
                        'weight': 50
                    }
                ],
                'page': 1,
                'pages': 1,
                'results': 1
            },
        )

    def domain_record_create(self):
        responses.post(
            self.host + '/v4/domains/1234/records',
            json={
                'created': '2018-01-01T00:01:01',
                'id': 123456,
                'name': 'test',
                'port': 80,
                'priority': 50,
                'protocol': None,
                'service': None,
                'tag': None,
                'target': '192.0.2.0',
                'ttl_sec': 604800,
                'type': 'A',
                'updated': '2018-01-01T00:01:01',
                'weight': 50
            },
        )

    def domain_record_delete(self):
        responses.delete(
            self.host + '/v4/domains/1234/records/123456',
            json={},
        )

    def domain_record_view(self):
        responses.get(
            self.host + '/v4/domains/1234/records/123456',
            json={
                'created': '2018-01-01T00:01:01',
                'id': 123456,
                'name': 'test',
                'port': 80,
                'priority': 50,
                'protocol': None,
                'service': None,
                'tag': None,
                'target': '192.0.2.0',
                'ttl_sec': 604800,
                'type': 'A',
                'updated': '2018-01-01T00:01:01',
                'weight': 50
            },
        )

    def domain_record_update(self):
        responses.put(
            self.host + '/v4/domains/1234/records/123456',
            json={
                'created': '2018-01-01T00:01:01',
                'id': 123456,
                'name': 'test',
                'port': 80,
                'priority': 50,
                'protocol': None,
                'service': None,
                'tag': None,
                'target': '192.0.2.0',
                'ttl_sec': 604800,
                'type': 'A',
                'updated': '2018-01-01T00:01:01',
                'weight': 50
            },
        )
