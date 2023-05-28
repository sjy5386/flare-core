class RecordError(Exception):
    pass


class RecordBadRequestError(RecordError):
    pass


class RecordNotFoundError(RecordError):
    pass


class RecordProviderError(RecordError):
    pass
