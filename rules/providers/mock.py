from typing import List

from subdomains.models import Subdomain
from .base import BaseProvider
from ..types import PageRule


class MockProvider(BaseProvider):
    i = 1
    rules = []

    def list_rules(self, subdomain: Subdomain) -> List[PageRule]:
        return self.rules

    def create_rule(self, subdomain: Subdomain, rule: PageRule) -> PageRule:
        rule.identifier = self.i
        self.i += 1
        self.rules.append(rule)
        return rule

    def retrieve_rule(self, subdomain: Subdomain, identifier) -> PageRule:
        for r in self.rules:
            if r.identifier == identifier:
                return r

    def update_rule(self, subdomain: Subdomain, identifier, rule: PageRule) -> PageRule:
        for r in self.rules:
            if r.identifier == identifier:
                r = rule
                r.identifier = identifier
                return r

    def delete_rule(self, subdomain: Subdomain, identifier):
        for r in self.rules:
            if r.identifier == identifier:
                self.rules.remove(r)
                return
