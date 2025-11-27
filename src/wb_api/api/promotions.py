"""Promotions API (Promotions Calendar) - READ operations only."""

from ..constants import DOMAINS, SANDBOX_DOMAINS
from ..models.promotions import Promotion, PromotionDetails, PromotionItem
from .base import BaseAPI


class PromotionsAPI(BaseAPI):
    """API for promotions calendar (read-only operations)."""

    @property
    def domain(self) -> str:
        """Get API domain."""
        if self._sandbox:
            return SANDBOX_DOMAINS.get("promotion", DOMAINS["promotion"])
        return DOMAINS["promotion"]

    def get_promotions_list(self) -> list[Promotion]:
        """Get list of promotions from calendar.

        Returns:
            List of Promotion objects with basic info.

        Rate limit: 60 requests/minute
        """
        data = self._get("/api/v1/calendar/promotions")
        promotions = data.get("data", [])
        return [Promotion(**item) for item in promotions]

    def get_promotions_details(self, promotion_id: int) -> PromotionDetails:
        """Get detailed information about specific promotion.

        Args:
            promotion_id: Promotion ID.

        Returns:
            PromotionDetails object.

        Rate limit: 60 requests/minute
        """
        params = {"id": promotion_id}
        data = self._get("/api/v1/calendar/promotions/details", params=params)
        return PromotionDetails(**data)

    def get_promotion_items(self, promotion_id: int) -> list[PromotionItem]:
        """Get items available for specific promotion.

        Args:
            promotion_id: Promotion ID.

        Returns:
            List of PromotionItem objects.

        Rate limit: 60 requests/minute
        """
        params = {"id": promotion_id}
        data = self._get("/api/v1/calendar/promotions/nomenclatures", params=params)
        items = data.get("data", [])
        return [PromotionItem(**item) for item in items]
