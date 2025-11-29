"""Tests for Statistics API."""


from wb_api.api.statistics import StatisticsAPI


def test_statistics_api_has_methods():
    """Test that StatisticsAPI has all required methods."""
    methods = [
        "get_sales_report",
        "iter_sales_report",
    ]

    for method in methods:
        assert hasattr(StatisticsAPI, method)


def test_statistics_api_domain():
    """Test StatisticsAPI domain property."""
    from wb_api import WildberriesClient

    client = WildberriesClient(token="test_token", sandbox=False)
    assert client.statistics.domain == "statistics-api.wildberries.ru"

    client_sandbox = WildberriesClient(token="test_token", sandbox=True)
    assert client_sandbox.statistics.domain == "statistics-api-sandbox.wildberries.ru"


def test_client_has_statistics_api():
    """Test that client has statistics API."""
    from wb_api import WildberriesClient

    client = WildberriesClient(token="test_token")
    assert hasattr(client, "statistics")
    assert isinstance(client.statistics, StatisticsAPI)
