class ShortUrlError(Exception):
    pass


class ShortUrlNotFoundError(ShortUrlError):
    pass


class ShortUrlProviderError(ShortUrlError):
    pass
