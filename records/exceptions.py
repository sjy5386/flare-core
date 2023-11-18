class DnsRecordError(Exception):
    pass


class DnsRecordBadRequestError(DnsRecordError):
    pass


class DnsRecordNotFoundError(DnsRecordError):
    pass


class DnsRecordProviderError(DnsRecordError):
    pass
