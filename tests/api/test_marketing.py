"""Tests for Marketing API."""


from wb_api.api.marketing import MarketingAPI


def test_marketing_api_has_methods():
    """Test that MarketingAPI has all required methods."""
    methods = [
        # Campaigns
        "list_campaigns",
        "get_campaigns_info",
        "get_auction_campaigns",
        # Statistics
        "get_full_stats",
        "get_daily_stats",
        "get_keyword_stats",
        "get_auto_cluster_stats",
        "get_cluster_stats",
        # Finance
        "get_balance",
        "get_campaign_budget",
        "get_expenses_history",
        "get_payments_history",
    ]

    for method in methods:
        assert hasattr(MarketingAPI, method)


def test_marketing_api_domain():
    """Test MarketingAPI domain property."""
    from wb_api import WildberriesClient

    client = WildberriesClient(token="test_token", sandbox=False)
    assert client.marketing.domain == "advert-api.wildberries.ru"

    client_sandbox = WildberriesClient(token="test_token", sandbox=True)
    assert client_sandbox.marketing.domain == "advert-api-sandbox.wildberries.ru"


def test_client_has_marketing_api():
    """Test that client has marketing API."""
    from wb_api import WildberriesClient

    client = WildberriesClient(token="test_token")
    assert hasattr(client, "marketing")
    assert isinstance(client.marketing, MarketingAPI)
