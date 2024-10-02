import requests
from requests.adapters import HTTPAdapter
from .config import IterableConfig
from .resources import UsersResource, EventsResource, WorkflowResource
from .exceptions import (
    IterableAPIException,
    RateLimitException,
    AuthenticationException,
)
import logging

logger = logging.getLogger(__name__)


class IterableClient:
    def __init__(self, config: IterableConfig):
        self.config = config
        self.session = self._create_session()

        self.users = UsersResource(self)
        self.events = EventsResource(self)
        self.workflows = WorkflowResource(self)

    def _create_session(self):
        session = requests.Session()
        adapter = HTTPAdapter(max_retries=self.config.max_retries)
        session.mount("https://", adapter)
        session.headers.update({"Api-Key": self.config.api_key})
        return session

    def request(self, method, endpoint, data=None, params=None):
        url = self.config.get_full_url(endpoint)
        # self.rate_limiter.wait() # currently disabled as we are using celery cooldowns

        try:
            response = self.session.request(
                method, url, json=data, params=params, timeout=self.config.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                raise RateLimitException("Rate limit exceeded", response=e.response)
            elif e.response.status_code == 401:
                raise AuthenticationException(
                    "Authentication failed", response=e.response
                )
            else:
                raise IterableAPIException(
                    f"HTTP error occurred: {e}", response=e.response
                )
        except requests.exceptions.RequestException as e:
            raise IterableAPIException(f"An error occurred: {e}")

    def get(self, endpoint, params=None):
        return self.request("GET", endpoint, params=params)

    def post(self, endpoint, data=None):
        return self.request("POST", endpoint, data=data)

    def delete(self, endpoint, data=None):
        return self.request("DELETE", endpoint, data=data)
