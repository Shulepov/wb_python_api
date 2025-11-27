"""Tests for Promotions API."""


from wb_api.api.promotions import PromotionsAPI


def test_promotions_api_has_methods():
    """Test that PromotionsAPI has all required methods."""
    methods = [
        "get_promotions_list",
        "get_promotions_details",
        "get_promotion_items",
    ]

    for method in methods:
        assert hasattr(PromotionsAPI, method)


def test_promotions_api_domain():
    """Test PromotionsAPI domain property."""
    from wb_api import WildberriesClient

    client = WildberriesClient(token="test_token", sandbox=False)
    assert client.promotions.domain == "advert-api.wildberries.ru"

    client_sandbox = WildberriesClient(token="test_token", sandbox=True)
    assert client_sandbox.promotions.domain == "advert-api-sandbox.wildberries.ru"


def test_client_has_promotions_api():
    """Test that client has promotions API."""
    from wb_api import WildberriesClient

    client = WildberriesClient(token="test_token")
    assert hasattr(client, "promotions")
    assert isinstance(client.promotions, PromotionsAPI)
