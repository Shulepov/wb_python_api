"""Tests for Finance API."""

import pytest

from wb_api.api.finance import FinanceAPI


def test_finance_api_has_methods():
    """Test that FinanceAPI has all required methods."""
    methods = [
        "get_balance",
    ]

    for method in methods:
        assert hasattr(FinanceAPI, method)


def test_finance_api_domain():
    """Test FinanceAPI domain property."""
    from wb_api import WildberriesClient

    client = WildberriesClient(token="test_token", sandbox=False)
    assert client.finance.domain == "finance-api.wildberries.ru"


def test_client_has_finance_api():
    """Test that client has finance API."""
    from wb_api import WildberriesClient

    client = WildberriesClient(token="test_token")
    assert hasattr(client, "finance")
    assert isinstance(client.finance, FinanceAPI)
