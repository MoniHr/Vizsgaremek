import pytest
from django.test import Client


@pytest.fixture
def http_client() -> Client:
    client = Client(enforce_csrf_checks=False)
    return client
