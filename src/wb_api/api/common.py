"""Common API for general operations."""

from typing import Any

from ..constants import DOMAINS
from ..models.seller_info import SellerInfo
from .base import BaseAPI


class CommonAPI(BaseAPI):
    """API for common operations (ping, tariffs, news, seller info)."""

    @property
    def domain(self) -> str:
        """Get domain for Common API."""
        return DOMAINS["common"]

    def ping(self) -> dict[str, Any]:
        """
        Check API connection.

        Returns:
            Response data
        """
        return self._get("/ping")

    def get_tariffs(self) -> dict[str, Any]:
        """
        Get tariffs information.

        Returns:
            Tariffs data
        """
        return self._get("/api/v1/tariffs/box")

    def get_tariffs_commission(self) -> dict[str, Any]:
        """
        Get commission tariffs.

        Returns:
            Commission data
        """
        return self._get("/api/v1/tariffs/commission")

    def get_seller_info(self) -> SellerInfo:
        """
        Get seller information.

        Returns information about the seller including legal name,
        seller ID, and trade name.

        Rate limits:
            - 1 request per minute
            - Burst: 10 requests

        Returns:
            SellerInfo: Seller information containing name, sid, and trade_mark

        Raises:
            WBAuthError: If token is invalid or unauthorized
            WBRateLimitError: If rate limit is exceeded

        Example:
            >>> seller = client.common.get_seller_info()
            >>> print(f"Seller: {seller.trade_mark} ({seller.name})")
            >>> print(f"SID: {seller.sid}")
        """
        data = self._get("/api/v1/seller-info")
        return SellerInfo(**data)
