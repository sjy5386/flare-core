import responses


class MockVultrDnsRecord:
    host = 'https://api.vultr.com'

    def __init__(self):
        self.create_record()
        self.list_records()
        self.get_record()
        self.update_record()
        self.delete_record()

    def create_record(self):
        responses.post(
            self.host + '/v2/domains/example.com/records',
            json={
                'record': {
                    'id': 'cb676a46-66fd-4dfb-b839-443f2e6c0b60',
                    'type': 'A',
                    'name': 'www',
                    'data': '192.0.2.123',
                    'priority': 0,
                    'ttl': 300,
                }
            },
            status=201,
        )

    def list_records(self):
        responses.get(
            self.host + '/v2/domains/example.com/records',
            json={
                'records': [
                    {
                        'id': 'cb676a46-66fd-4dfb-b839-443f2e6c0b60',
                        'type': 'A',
                        'name': 'foo.example.com',
                        'data': '192.0.2.123',
                        'priority': 0,
                        'ttl': 300,
                    }
                ],
                'meta': {
                    'total': 1,
                    'links': {
                        'next': '',
                        'prev': '',
                    }
                }
            }
        )

    def get_record(self):
        responses.get(
            self.host + '/v2/domains/example.com/records/cb676a46-66fd-4dfb-b839-443f2e6c0b60',
            json={
                'record': {
                    'id': 'cb676a46-66fd-4dfb-b839-443f2e6c0b60',
                    'type': 'A',
                    'name': 'www',
                    'data': '192.0.2.123',
                    'priority': 0,
                    'ttl': 300,
                }
            }
        )

    def update_record(self):
        responses.patch(
            self.host + '/v2/domains/example.com/records/cb676a46-66fd-4dfb-b839-443f2e6c0b60',
            status=204,
        )

    def delete_record(self):
        responses.delete(
            self.host + '/v2/domains/example.com/records/cb676a46-66fd-4dfb-b839-443f2e6c0b60',
            status=204,
        )
