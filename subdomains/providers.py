from typing import List

from .models import Subdomain
from .types import Record


class BaseProvider:
    def list_records(self, subdomain: Subdomain) -> List[Record]:
        pass

    def create_record(self, subdomain: Subdomain, record: Record) -> Record:
        pass

    def retrieve_record(self, subdomain: Subdomain, identifier) -> Record:
        pass

    def update_record(self, subdomain: Subdomain, identifier, record: Record) -> Record:
        pass

    def delete_record(self, subdomain: Subdomain, identifier):
        pass
