"""Tests for Reports API."""


from wb_api.api.reports import ReportsAPI


def test_reports_api_has_methods():
    """Test that ReportsAPI has all required methods."""
    methods = [
        # Basic reports
        "get_incomes",
        "get_stocks",
        "get_orders",
        "get_sales",
        # Excise report
        "get_excise_report",
        # Deduction reports
        "get_warehouse_measurements",
        "get_antifraud_details",
        "get_incorrect_attachments",
        "get_goods_labeling",
        "get_characteristics_change",
        # Region sales
        "get_region_sales",
        # Brand share
        "get_brand_list",
        "get_parent_subjects",
        "get_brand_share",
        # Generated reports
        "create_warehouse_remains",
        "check_warehouse_remains_status",
        "download_warehouse_remains",
        "wait_for_warehouse_remains",
        "create_acceptance_report",
        "check_acceptance_status",
        "download_acceptance_report",
        "wait_for_acceptance_report",
        "create_paid_storage",
        "check_paid_storage_status",
        "download_paid_storage",
        "wait_for_paid_storage",
    ]

    for method in methods:
        assert hasattr(ReportsAPI, method)


def test_reports_api_domain():
    """Test ReportsAPI domain property."""
    from wb_api import WildberriesClient

    client = WildberriesClient(token="test_token", sandbox=False)
    assert client.reports.domain == "statistics-api.wildberries.ru"

    client_sandbox = WildberriesClient(token="test_token", sandbox=True)
    assert client_sandbox.reports.domain == "statistics-api-sandbox.wildberries.ru"


def test_client_has_reports_api():
    """Test that client has reports API."""
    from wb_api import WildberriesClient

    client = WildberriesClient(token="test_token")
    assert hasattr(client, "reports")
    assert isinstance(client.reports, ReportsAPI)
