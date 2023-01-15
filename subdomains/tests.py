from django.core.exceptions import ValidationError
from django.test import TestCase

from subdomains.validators import validate_domain_name


class SubdomainTest(TestCase):
    def test_validate_subdomain_name(self):
        success_values = (
            'helloworld', 'hello-world', 'helloworld1',
        )
        failure_values = (
            'helloworld-', 'Hello, world!', '안녕세상',
        )
        for value in success_values:
            validate_domain_name(value)
        with self.assertRaises(ValidationError):
            for value in failure_values:
                validate_domain_name(value)
