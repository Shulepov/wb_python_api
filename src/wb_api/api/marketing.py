"""Marketing API (Advertising/Promotion) - READ operations only."""

from datetime import date, datetime

from ..constants import DOMAINS, SANDBOX_DOMAINS
from ..models.marketing import (
    Balance,
    CampaignBudget,
    CampaignInfo,
    CampaignListResponse,
    CampaignStats,
    ClusterStats,
    DailyStats,
    Expense,
    KeywordStats,
    Payment,
)
from .base import BaseAPI


class MarketingAPI(BaseAPI):
    """API for advertising campaigns (read-only operations)."""

    @property
    def domain(self) -> str:
        """Get API domain."""
        if self._sandbox:
            return SANDBOX_DOMAINS.get("promotion", DOMAINS["promotion"])
        return DOMAINS["promotion"]

    # === Campaigns ===

    def list_campaigns(self) -> CampaignListResponse:
        """Get list of all advertising campaigns with their IDs.

        Returns:
            CampaignListResponse with lists of campaign IDs by status.

        Rate limit: 60 requests/minute
        """
        data = self._get("/adv/v1/promotion/count")
        return CampaignListResponse(**data)

    def get_campaigns_info(self, campaign_ids: list[int]) -> list[CampaignInfo]:
        """Get detailed information about campaigns (type 8 - unified bid).

        Args:
            campaign_ids: List of campaign IDs to get info for.

        Returns:
            List of CampaignInfo objects.

        Rate limit: 60 requests/minute
        """
        data = self._post("/adv/v1/promotion/adverts", json=campaign_ids)
        return [CampaignInfo(**item) for item in data]

    def get_auction_campaigns(
        self,
        status: int | None = None,
        type_: int | None = None,
    ) -> list[CampaignInfo]:
        """Get information about auction campaigns (manual bid).

        Args:
            status: Filter by campaign status (4, 7, 9, 11).
            type_: Filter by campaign type (4, 5, 6, 7, 9).

        Returns:
            List of CampaignInfo objects.

        Rate limit: 60 requests/minute
        """
        params = {}
        if status is not None:
            params["status"] = status
        if type_ is not None:
            params["type"] = type_

        data = self._get("/adv/v0/auction/adverts", params=params)
        return [CampaignInfo(**item) for item in data]

    # === Statistics ===

    def get_full_stats(
        self,
        campaign_ids: list[int],
        date_from: date | datetime,
        date_to: date | datetime,
    ) -> list[CampaignStats]:
        """Get campaign statistics for specified period.

        Args:
            campaign_ids: List of campaign IDs (max 100).
            date_from: Start date.
            date_to: End date.

        Returns:
            List of CampaignStats objects.

        Rate limit: 60 requests/minute
        """
        if isinstance(date_from, datetime):
            date_from = date_from.date()
        if isinstance(date_to, datetime):
            date_to = date_to.date()

        params = {
            "id": campaign_ids,
            "dateFrom": date_from.isoformat(),
            "dateTo": date_to.isoformat(),
        }

        data = self._get("/adv/v3/fullstats", params=params)
        stats = []
        for item in data:
            item["date_from"] = date_from
            item["date_to"] = date_to
            stats.append(CampaignStats(**item))
        return stats

    def get_daily_stats(
        self,
        campaign_ids: list[int],
        date_from: date | datetime,
        date_to: date | datetime,
    ) -> list[DailyStats]:
        """Get daily campaign statistics for specified period.

        Args:
            campaign_ids: List of campaign IDs (max 100).
            date_from: Start date.
            date_to: End date.

        Returns:
            List of DailyStats objects (one per campaign per day).

        Rate limit: 60 requests/minute
        """
        if isinstance(date_from, datetime):
            date_from = date_from.date()
        if isinstance(date_to, datetime):
            date_to = date_to.date()

        params = {
            "id": campaign_ids,
            "dateFrom": date_from.isoformat(),
            "dateTo": date_to.isoformat(),
        }

        # Using POST method for fullstats with additional params
        data = self._post("/adv/v2/fullstats", json=params)
        return [DailyStats(**item) for item in data]

    def get_keyword_stats(self, campaign_id: int) -> list[KeywordStats]:
        """Get keyword statistics for manual bid campaign.

        Args:
            campaign_id: Campaign ID.

        Returns:
            List of KeywordStats objects.

        Rate limit: 60 requests/minute
        """
        params = {"id": campaign_id}
        data = self._get("/adv/v1/stat/words", params=params)
        keywords = data.get("keywords", [])
        return [KeywordStats(**item) for item in keywords]

    def get_auto_cluster_stats(self, campaign_id: int) -> list[ClusterStats]:
        """Get cluster statistics for unified bid campaign.

        Args:
            campaign_id: Campaign ID (type 8).

        Returns:
            List of ClusterStats objects.

        Rate limit: 60 requests/minute
        """
        params = {"id": campaign_id}
        data = self._get("/adv/v2/auto/stat-words", params=params)
        return [ClusterStats(**item) for item in data]

    def get_cluster_stats(
        self,
        campaign_id: int,
        date_from: date | datetime,
        date_to: date | datetime,
    ) -> list[ClusterStats]:
        """Get search cluster statistics for specified period.

        Args:
            campaign_id: Campaign ID.
            date_from: Start date.
            date_to: End date.

        Returns:
            List of ClusterStats objects.

        Rate limit: 60 requests/minute
        """
        if isinstance(date_from, datetime):
            date_from = date_from.date()
        if isinstance(date_to, datetime):
            date_to = date_to.date()

        payload = {
            "id": campaign_id,
            "dateFrom": date_from.isoformat(),
            "dateTo": date_to.isoformat(),
        }

        data = self._post("/adv/v0/normquery/stats", json=payload)
        return [ClusterStats(**item) for item in data]

    # === Finance ===

    def get_balance(self) -> Balance:
        """Get current advertising account balance.

        Returns:
            Balance object with current balance info.

        Rate limit: 60 requests/minute
        """
        data = self._get("/adv/v1/balance")
        return Balance(**data)

    def get_campaign_budget(self, campaign_id: int) -> CampaignBudget:
        """Get campaign budget information.

        Args:
            campaign_id: Campaign ID.

        Returns:
            CampaignBudget object.

        Rate limit: 60 requests/minute
        """
        params = {"id": campaign_id}
        data = self._get("/adv/v1/budget", params=params)
        data["campaign_id"] = campaign_id
        return CampaignBudget(**data)

    def get_expenses_history(
        self,
        date_from: date | datetime,
        date_to: date | datetime,
    ) -> list[Expense]:
        """Get advertising expenses history for specified period.

        Args:
            date_from: Start date.
            date_to: End date.

        Returns:
            List of Expense objects.

        Rate limit: 60 requests/minute
        """
        if isinstance(date_from, datetime):
            date_from = date_from.date()
        if isinstance(date_to, datetime):
            date_to = date_to.date()

        params = {
            "dateFrom": date_from.isoformat(),
            "dateTo": date_to.isoformat(),
        }

        data = self._get("/adv/v1/upd", params=params)
        return [Expense(**item) for item in data]

    def get_payments_history(
        self,
        date_from: date | datetime,
        date_to: date | datetime,
    ) -> list[Payment]:
        """Get advertising payments history for specified period.

        Args:
            date_from: Start date.
            date_to: End date.

        Returns:
            List of Payment objects.

        Rate limit: 60 requests/minute
        """
        if isinstance(date_from, datetime):
            date_from = date_from.date()
        if isinstance(date_to, datetime):
            date_to = date_to.date()

        params = {
            "dateFrom": date_from.isoformat(),
            "dateTo": date_to.isoformat(),
        }

        data = self._get("/adv/v1/payments", params=params)
        return [Payment(**item) for item in data]
