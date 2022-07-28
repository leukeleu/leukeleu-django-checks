# Not sentry-sdk, but just enough stubbing to make the tests work


class Client:
    def __init__(self, *args, **options):
        self.dsn = options.get("dsn")


class Hub:
    def __init__(self, client=None):
        self.client = client


Hub.current = Hub()
