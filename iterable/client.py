import json
import logging
from decimal import Decimal

import requests
from requests.adapters import HTTPAdapter
from .config import IterableConfig
from .resources import UsersResource, EventsResource, WorkflowResource, CommerceResource, CatalogResource
from .exceptions import (
    IterableAPIException,
    RateLimitException,
    AuthenticationException,
)

logger = logging.getLogger(__name__)


def _encode_json_value(value):
    """json.dumps default hook: Decimal is the one non-JSON type our callers
    legitimately send (Django DecimalFields — prices, totals). Everything
    else stays a TypeError so malformed payloads fail fast."""
    if isinstance(value, Decimal):
        return float(value)
    raise TypeError(
        f"Object of type {value.__class__.__name__} is not JSON serializable"
    )


class IterableClient:
    def __init__(self, config: IterableConfig):
        self.config = config
        self.session = self._create_session()

        self.commerce = CommerceResource(self)
        self.events = EventsResource(self)
        self.users = UsersResource(self)
        self.workflows = WorkflowResource(self)
        self.catalog = CatalogResource(self)

    def _create_session(self):
        session = requests.Session()
        adapter = HTTPAdapter(max_retries=self.config.max_retries)
        session.mount("https://", adapter)
        session.headers.update({"Api-Key": self.config.api_key})
        return session

    def request(self, method, endpoint, data=None, params=None):
        url = self.config.get_full_url(endpoint)
        # self.rate_limiter.wait() # currently disabled as we are using celery cooldowns

        # Encode the body here instead of passing json= to requests: requests
        # delegates to simplejson when the host environment happens to have it
        # installed and to the stdlib json module when it doesn't, and the two
        # disagree on Decimal. Encoding here pins one behavior regardless of
        # the host environment. allow_nan=False matches requests' json= path.
        body = None
        headers = None
        if data is not None:
            body = json.dumps(data, allow_nan=False, default=_encode_json_value)
            headers = {"Content-Type": "application/json"}

        try:
            response = self.session.request(
                method,
                url,
                data=body,
                headers=headers,
                params=params,
                timeout=self.config.timeout,
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
