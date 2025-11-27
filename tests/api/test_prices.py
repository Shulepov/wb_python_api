"""Tests for Prices API."""


from wb_api.api.prices import PricesAPI


def test_prices_api_has_methods():
    """Test that PricesAPI has all required methods."""
    methods = [
        "upload_prices",
        "upload_size_prices",
        "upload_club_discounts",
        "get_processed_tasks",
        "get_task_details",
        "get_pending_tasks",
        "get_pending_task_details",
        "wait_for_task",
        "get_goods_with_prices",
        "get_goods_by_vendor_codes",
        "get_size_prices",
        "get_quarantine_goods",
        "iter_goods_with_prices",
    ]

    for method in methods:
        assert hasattr(PricesAPI, method)


def test_prices_api_domain():
    """Test PricesAPI domain property."""
    from wb_api import WildberriesClient

    client = WildberriesClient(token="test_token", sandbox=False)
    assert client.prices.domain == "discounts-prices-api.wildberries.ru"

    client_sandbox = WildberriesClient(token="test_token", sandbox=True)
    assert client_sandbox.prices.domain == "discounts-prices-api-sandbox.wildberries.ru"


def test_client_has_prices_api():
    """Test that client has prices API."""
    from wb_api import WildberriesClient

    client = WildberriesClient(token="test_token")
    assert hasattr(client, "prices")
    assert isinstance(client.prices, PricesAPI)
