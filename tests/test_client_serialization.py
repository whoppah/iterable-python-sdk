"""Request-body encoding is pinned to the stdlib json module.

requests picks simplejson over stdlib json when the host environment happens
to have it installed, and the two disagree on Decimal — the Whoppah monolith's
Django 5.2 upgrade dropped simplejson from its lockfile and every purchase
payload carrying a DecimalField started raising TypeError. The client now
encodes bodies itself so behavior no longer depends on the host environment.
"""

import json
from decimal import Decimal
from unittest.mock import Mock

import pytest

from iterable.client import IterableClient
from iterable.config import IterableConfig


@pytest.fixture()
def client():
    client = IterableClient(config=IterableConfig(api_key="test-key"))
    response = Mock()
    response.json.return_value = {}
    response.raise_for_status.return_value = None
    client.session = Mock()
    client.session.request.return_value = response
    return client


def sent_body(client):
    return client.session.request.call_args.kwargs["data"]


def test_decimal_is_encoded_as_a_json_number(client):
    client.post("commerce/trackPurchase", data={"total": Decimal("12.50")})

    body = json.loads(sent_body(client))
    assert body == {"total": 12.5}


def test_content_type_header_is_set_when_a_body_is_sent(client):
    client.post("events/track", data={"eventName": "signup"})

    headers = client.session.request.call_args.kwargs["headers"]
    assert headers == {"Content-Type": "application/json"}


def test_no_body_and_no_content_type_without_data(client):
    client.get("users/getByEmail", params={"email": "a@b.c"})

    kwargs = client.session.request.call_args.kwargs
    assert kwargs["data"] is None
    assert kwargs["headers"] is None


def test_non_serializable_values_still_fail_fast(client):
    with pytest.raises(TypeError, match="not JSON serializable"):
        client.post("events/track", data={"when": object()})


def test_nan_still_fails_fast(client):
    # allow_nan=False matches what requests' json= path enforced.
    with pytest.raises(ValueError):
        client.post("events/track", data={"total": float("nan")})
