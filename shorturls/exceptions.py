class ShortUrlError(Exception):
    pass


class ShortUrlBadRequestError(ShortUrlError):
    pass


class ShortUrlNotFoundError(ShortUrlError):
    pass


class ShortUrlProviderError(ShortUrlError):
    pass
