from django.db import models

from domains.models import Domain


class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    provider_id = models.CharField(max_length=255, unique=True, null=True)

    subdomain_name = models.CharField(max_length=63)
    domain = models.ForeignKey(Domain)

    name = models.CharField('Name', max_length=63)
    ttl = models.IntegerField('TTL', default=3600)
    type = models.CharField('Type', max_length=10)
    # data = models.CharField('Data', max_length=255)

    # Required for SRV record.
    service = models.CharField('Service', max_length=63, null=True)
    # Required for SRV record.
    protocol = models.CharField('Protocol', max_length=63, null=True)

    # Required for MX and SRV records.
    priority = models.IntegerField('Priority', null=True)
    # Required for SRV record.
    weight = models.IntegerField('Weight', null=True)
    # Required for SRV record.
    port = models.IntegerField('Port', null=True)

    target = models.CharField('Target', max_length=255)

    @property
    def full_name(self) -> str:
        name = f'{self.name}.{self.subdomain_name}.{self.domain.name}'
        return name if self.type != 'SRV' else f'{self.service}.{self.protocol}.{name}'

    @property
    def data(self) -> str:
        return f'{self.priority} {self.weight} {self.port} {self.target}'.strip()

    def __str__(self):
        return f'{self.full_name} {self.ttl} IN {self.type} {self.data}'
