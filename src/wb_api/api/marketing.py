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
        """Get detailed information about campaigns.

        Args:
            campaign_ids: List of campaign IDs to get info for. Max 50

        Returns:
            List of CampaignInfo objects.

        Rate limit: 60 requests/minute
        """
        params = {"ids": ",".join(map(str, campaign_ids))}
        data = self._get("/api/advert/v2/adverts", params=params)
        adverts = data["adverts"]
        return [CampaignInfo(**item) for item in adverts]

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

    def get_keyword_stats(self, campaign_id: int) -> list[KeywordStats]:
        """Get keyword statistics for manual bid campaign.

        Args:
            campaign_id: Campaign ID.

        Returns:
            List of KeywordStats objects.

        Rate limit: 60 requests/minute
        """
        params = {"id": campaign_id}
        data = self._get("/adv/v2/auto/stat-words", params=params)
        return KeywordStats(**data)

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
        stats = data["stats"]
        return [ClusterStats(**item) for item in stats]

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

        Note: API has 31 days limit per request. This method automatically
        splits longer periods into 31-day chunks.

        Args:
            date_from: Start date.
            date_to: End date.

        Returns:
            List of Expense objects for the entire period.

        Rate limit: 60 requests/minute
        """
        from datetime import timedelta

        if isinstance(date_from, datetime):
            date_from = date_from.date()
        if isinstance(date_to, datetime):
            date_to = date_to.date()

        # Split into 31-day chunks (API limit: 31 days per request)
        all_expenses = []
        current_date = date_from

        while current_date <= date_to:
            # Calculate end of current chunk (max 31 days from current_date)
            chunk_end = min(current_date + timedelta(days=30), date_to)

            # Make request for this chunk
            params = {
                "from": current_date.isoformat(),
                "to": chunk_end.isoformat(),
            }

            data = self._get("/adv/v1/upd", params=params)
            if data:
                expenses = [Expense(**item) for item in data]
            all_expenses.extend(expenses)

            # Move to next chunk (start day after chunk_end)
            current_date = chunk_end + timedelta(days=1)

        return all_expenses

    def get_payments_history(
        self,
        date_from: date | datetime,
        date_to: date | datetime,
    ) -> list[Payment]:
        """Get advertising payments history for specified period.

        Note: API has 31 days limit per request. This method automatically
        splits longer periods into 31-day chunks.

        Args:
            date_from: Start date.
            date_to: End date.

        Returns:
            List of Payment objects for the entire period.

        Rate limit: 60 requests/minute
        """
        from datetime import timedelta

        if isinstance(date_from, datetime):
            date_from = date_from.date()
        if isinstance(date_to, datetime):
            date_to = date_to.date()

        # Split into 31-day chunks (API limit: 31 days per request)
        all_payments = []
        current_date = date_from

        while current_date <= date_to:
            # Calculate end of current chunk (max 31 days from current_date)
            chunk_end = min(current_date + timedelta(days=30), date_to)

            # Make request for this chunk
            params = {
                "from": current_date.isoformat(),
                "to": chunk_end.isoformat(),
            }

            data = self._get("/adv/v1/payments", params=params)
            if data:
                payments = [Payment(**item) for item in data]
            all_payments.extend(payments)

            # Move to next chunk (start day after chunk_end)
            current_date = chunk_end + timedelta(days=1)

        return all_payments
