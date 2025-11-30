"""Tests for Common API."""

from wb_api.api.common import CommonAPI


def test_common_api_has_methods():
    """Test that CommonAPI has all required methods."""
    methods = [
        "ping",
        "get_tariffs",
        "get_tariffs_commission",
        "get_seller_info",
    ]

    for method in methods:
        assert hasattr(CommonAPI, method)
