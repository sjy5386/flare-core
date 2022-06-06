from typing import List

from subdomains.models import Subdomain
from ..types import PageRule


class BaseProvider:
    def list_rules(self, subdomain: Subdomain) -> List[PageRule]:
        pass

    def create_rule(self, subdomain: Subdomain, rule: PageRule) -> PageRule:
        pass

    def retrieve_rule(self, subdomain: Subdomain, identifier) -> PageRule:
        pass

    def update_rule(self, subdomain: Subdomain, identifier, rule: PageRule) -> PageRule:
        pass

    def delete_rule(self, subdomain: Subdomain, identifier):
        pass
