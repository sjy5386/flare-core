import re

from django.db import models

from contacts.models import Contact
from domains.models import Domain
from base.settings.common import AUTH_USER_MODEL
from .validators import validate_domain_name


class Subdomain(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.RESTRICT)
    name = models.CharField(max_length=63, validators=[validate_domain_name])
    domain = models.ForeignKey(Domain, on_delete=models.RESTRICT)

    expiry = models.DateTimeField()

    registrant = models.ForeignKey(Contact, on_delete=models.RESTRICT, related_name='registrant_contact')
    admin = models.ForeignKey(Contact, on_delete=models.RESTRICT, related_name='admin_contact')
    tech = models.ForeignKey(Contact, on_delete=models.RESTRICT, related_name='tech_contact')
    billing = models.ForeignKey(Contact, on_delete=models.RESTRICT, related_name='billing_contact')
    is_private = models.BooleanField(default=True)

    records = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'domain'], name='unique_domain_name')
        ]

    def __str__(self):
        return self.name + '.' + self.domain.name

    @staticmethod
    def is_available(name: str, domain: Domain):
        name = name.lower()
        return 3 <= len(name) <= 63 and re.match('^[a-z0-9][a-z0-9-]*[a-z0-9]$', name) is not None and len(
            Subdomain.objects.filter(name=name, domain=domain)) == 0 and len(
            ReservedName.objects.filter(name=name)) == 0


class ReservedName(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=63, unique=True)

    def __str__(self):
        return self.name


class SubdomainStatus(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    subdomain = models.ForeignKey(Subdomain, on_delete=models.CASCADE)

    class StatusChoices(models.TextChoices):
        ADD_PERIOD = 'addPeriod', 'addPeriod'
        AUTO_RENEW_PERIOD = 'autoRenewPeriod', 'autoRenewPeriod'

        INACTIVE = 'inactive', 'inactive'
        OK = 'ok', 'ok'

        PENDING_CREATE = 'pendingCreate', 'pendingCreate'
        PENDING_DELETE = 'pendingDelete', 'pendingDelete'
        PENDING_RENEW = 'pendingRenew', 'pendingRenew'
        PENDING_RESTORE = 'pendingRestore', 'pendingRestore'
        PENDING_TRANSFER = 'pendingTransfer', 'pendingTransfer'
        PENDING_UPDATE = 'pendingUpdate', 'pendingUpdate'

        REDEMPTION_PERIOD = 'redemptionPeriod', 'redemptionPeriod'
        RENEW_PERIOD = 'renewPeriod', 'renewPeriod'
        TRANSFER_PERIOD = 'transferPeriod', 'transferPeriod'

        SERVER_DELETE_PROHIBITED = 'serverDeleteProhibited', 'serverDeleteProhibited'
        SERVER_HOLD = 'serverHold', 'serverHold'
        SERVER_RENEW_PROHIBITED = 'serverRenewProhibited', 'serverRenewProhibited'
        SERVER_TRANSFER_PROHIBITED = 'serverTransferProhibited', 'serverTransferProhibited'
        SERVER_UPDATE_PROHIBITED = 'serverUpdateProhibited', 'serverUpdateProhibited'

        CLIENT_DELETE_PROHIBITED = 'clientDeleteProhibited', 'clientDeleteProhibited'
        CLIENT_HOLD = 'clientHold', 'clientHold'
        CLIENT_RENEW_PROHIBITED = 'clientRenewProhibited', 'clientRenewProhibited'
        CLIENT_TRANSFER_PROHIBITED = 'clientTransferProhibited', 'clientTransferProhibited'
        CLIENT_UPDATE_PROHIBITED = 'clientUpdateProhibited', 'clientUpdateProhibited'

    status = models.CharField(max_length=31, choices=StatusChoices.choices, default=StatusChoices.OK)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['subdomain', 'status'], name='unique_subdomain_status')
        ]

    def __str__(self):
        return f'{self.subdomain} {self.status}'
