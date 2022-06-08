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
        rule.id = self.i
        self.i += 1
        self.rules.append(rule)
        return rule

    def retrieve_rule(self, subdomain: Subdomain, id) -> PageRule:
        for r in self.rules:
            if r.id == id:
                return r

    def update_rule(self, subdomain: Subdomain, id, rule: PageRule) -> PageRule:
        for r in self.rules:
            if r.id == id:
                r = rule
                r.id = id
                return r

    def delete_rule(self, subdomain: Subdomain, id):
        for r in self.rules:
            if r.id == id:
                self.rules.remove(r)
                return
