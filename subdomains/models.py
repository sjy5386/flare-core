import datetime

from django.db import models

from contacts.models import Contact
from domains.models import Domain
from base.settings import AUTH_USER_MODEL


class Subdomain(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.RESTRICT)
    name = models.CharField(max_length=63)
    domain = models.ForeignKey(Domain, on_delete=models.RESTRICT)

    expiry = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(days=90))

    class StatusChoices(models.TextChoices):
        ADD_PERIOD = 'addPeriod', 'add period'
        AUTO_RENEW_PERIOD = 'autoRenewPeriod', 'auto renew period'

        INACTIVE = 'inactive', 'inactive'
        OK = 'ok', 'active'

        PENDING_CREATE = 'pendingCreate', 'pending create'
        PENDING_DELETE = 'pendingDelete', 'pending delete'
        PENDING_RENEW = 'pendingRenew', 'pending renew'
        PENDING_RESTORE = 'pendingRestore', 'pending restore'
        PENDING_TRANSFER = 'pendingTransfer', 'pending transfer'
        PENDING_UPDATE = 'pendingUpdate', 'pending update'

        REDEMPTION_PERIOD = 'redemptionPeriod', 'redemption period'
        RENEW_PERIOD = 'renewPeriod', 'renew period'
        TRANSFER_PERIOD = 'transferPeriod', 'transfer period'

        SERVER_DELETE_PROHIBITED = 'serverDeleteProhibited', 'server delete prohibited'
        SERVER_HOLD = 'serverHold', 'server hold'
        SERVER_RENEW_PROHIBITED = 'serverRenewProhibited', 'server renew prohibited'
        SERVER_TRANSFER_PROHIBITED = 'serverTransferProhibited', 'server transfer prohibited'
        SERVER_UPDATE_PROHIBITED = 'serverUpdateProhibited', 'server update prohibited'

        CLIENT_DELETE_PROHIBITED = 'clientDeleteProhibited', 'client delete prohibited'
        CLIENT_HOLD = 'clientHold', 'client hold'
        CLIENT_RENEW_PROHIBITED = 'clientRenewProhibited', 'client renew prohibited'
        CLIENT_TRANSFER_PROHIBITED = 'clientTransferProhibited', 'client transfer prohibited'
        CLIENT_UPDATE_PROHIBITED = 'clientUpdateProhibited', 'client update prohibited'

    status = models.CharField(max_length=31, choices=StatusChoices.choices, default=StatusChoices.OK)

    registrant = models.ForeignKey(Contact, on_delete=models.RESTRICT, related_name='registrant_contact')
    admin = models.ForeignKey(Contact, on_delete=models.RESTRICT, related_name='admin_contact')
    tech = models.ForeignKey(Contact, on_delete=models.RESTRICT, related_name='tech_contact', null=True)
    billing = models.ForeignKey(Contact, on_delete=models.RESTRICT, related_name='billing_contact', null=True)
    is_private = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'domain'], name='unique_domain_name')
        ]

    def __str__(self):
        return self.name + '.' + self.domain.name
