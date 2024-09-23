from urllib.parse import urljoin

class IterableConfig:
    def __init__(
            self,
            api_key,
            base_url="https://api.eu.iterable.com/api/",
            timeout=30,
            max_retries=3,
            backoff_factor=0.3
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def get_full_url(self, endpoint):
        return urljoin(self.base_url, endpoint)

