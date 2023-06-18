import requests


class DynamicDnsClient:
    def __init__(self, token: str, host: str = 'https://subshorts.com', endpoint: str = 'dynamic-dns'):
        self.token = token
        self.host = host
        self.endpoint = endpoint

    def retrieve(self) -> str:
        return requests.get(f'{self.host}/{self.endpoint}/{self.token}/').text

    def update(self) -> str:
        return requests.post(f'{self.host}/{self.endpoint}/{self.token}/').text
