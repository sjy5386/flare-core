class RecordError(Exception):
    pass


class RecordNotFoundError(RecordError):
    pass


class RecordProviderError(RecordError):
    pass
