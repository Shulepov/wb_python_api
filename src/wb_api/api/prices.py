"""Prices API for managing prices and discounts."""

from collections.abc import Callable, Iterator
from typing import Any

from ..constants import DOMAINS, SANDBOX_DOMAINS
from ..models.prices import (
    GoodPrice,
    GoodSize,
    QuarantineGood,
)
from .base import BaseAPI


class PricesAPI(BaseAPI):
    """API for working with prices and discounts."""

    @property
    def domain(self) -> str:
        """Get domain for Prices API."""
        if self._sandbox:
            return SANDBOX_DOMAINS.get("prices", DOMAINS["prices"])
        return DOMAINS["prices"]

    # === Get Prices ===

    def get_goods_with_prices(
        self, limit: int = 1000, offset: int = 0
    ) -> list[GoodPrice]:
        """
        Get all products with current prices.

        Args:
            limit: Maximum number of products to return (max 1000)
            offset: Offset for pagination

        Returns:
            List of GoodPrice objects

        Example:
            >>> goods = client.prices.get_goods_with_prices(limit=100)
            >>> for good in goods:
            ...     print(f"{good.vendor_code}: {good.price}₽ (-{good.discount}%)")
        """
        params = {"limit": min(limit, 1000), "offset": offset}
        data = self._get("/api/v2/list/goods/filter", params=params)
        if not data or "data" not in data:
            return []
        return [GoodPrice(**item) for item in data["data"]["listGoods"]]

    def get_goods_by_vendor_codes(
        self, vendor_codes: list[str]
    ) -> list[GoodPrice]:
        """
        Get products with prices filtered by vendor codes.

        Args:
            vendor_codes: List of vendor codes (max 1000)

        Returns:
            List of GoodPrice objects

        Example:
            >>> goods = client.prices.get_goods_by_vendor_codes(["ART-001", "ART-002"])
            >>> for good in goods:
            ...     print(f"{good.vendor_code}: {good.price}₽")
        """
        if not vendor_codes:
            return []

        payload = {"vendorCodes": vendor_codes[:1000]}
        data = self._post("/api/v2/list/goods/filter", json=payload)
        if not data or "data" not in data:
            return []
        return [GoodPrice(**item) for item in data["data"]]

    def get_size_prices(self, nm_id: int) -> list[GoodSize]:
        """
        Get prices for all sizes of a product.

        Args:
            nm_id: Nomenclature ID

        Returns:
            List of GoodSize objects

        Example:
            >>> sizes = client.prices.get_size_prices(nm_id=123456)
            >>> for size in sizes:
            ...     print(f"Size {size.tech_size}: {size.price}₽")
        """
        params = {"nmId": nm_id}
        data = self._get("/api/v2/list/goods/size/nm", params=params)
        if not data or "data" not in data:
            return []
        return [GoodSize(**item) for item in data["data"]]

    def get_quarantine_goods(self) -> list[QuarantineGood]:
        """
        Get products in quarantine (with price issues).

        Returns:
            List of QuarantineGood objects

        Example:
            >>> quarantine = client.prices.get_quarantine_goods()
            >>> for good in quarantine:
            ...     print(f"{good.vendor_code}: {good.reason}")
        """
        data = self._get("/api/v2/quarantine/goods")
        if not data or "data" not in data:
            return []
        return [QuarantineGood(**item) for item in data["data"]]

    # === Convenience Methods ===

    def iter_goods_with_prices(
        self, batch_size: int = 1000, **filters: Any
    ) -> Iterator[GoodPrice]:
        """
        Iterate over all products with prices using automatic pagination.

        Args:
            batch_size: Number of products per request (max 1000)
            **filters: Additional filters

        Yields:
            GoodPrice objects

        Example:
            >>> for good in client.prices.iter_goods_with_prices(batch_size=500):
            ...     print(f"{good.nm_id}: {good.price}₽")
        """
        offset = 0
        batch_size = min(batch_size, 1000)

        while True:
            goods = self.get_goods_with_prices(
                limit=batch_size, offset=offset, **filters
            )

            if not goods:
                break

            yield from goods

            if len(goods) < batch_size:
                break

            offset += batch_size
