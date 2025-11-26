"""Prices API for managing prices and discounts."""

from collections.abc import Callable, Iterator
from typing import Any

from ..constants import DOMAINS, SANDBOX_DOMAINS
from ..models.prices import (
    BufferTask,
    ClubDiscount,
    GoodPrice,
    GoodSize,
    HistoryTask,
    Price,
    PriceTaskDetails,
    QuarantineGood,
    SizePrice,
    UploadTaskResponse,
)
from .base import BaseAPI
from .tasks import TaskAPIMixin


class PricesAPI(BaseAPI, TaskAPIMixin):
    """API for working with prices and discounts."""

    @property
    def domain(self) -> str:
        """Get domain for Prices API."""
        if self._sandbox:
            return SANDBOX_DOMAINS.get("prices", DOMAINS["prices"])
        return DOMAINS["prices"]

    # === Upload Prices ===

    def upload_prices(self, prices: list[Price]) -> UploadTaskResponse:
        """
        Upload prices and discounts for products.

        Args:
            prices: List of Price objects

        Returns:
            UploadTaskResponse with task_id

        Example:
            >>> prices = [
            ...     Price(nm_id=123456, price=1500, discount=20),
            ...     Price(nm_id=123457, price=2000, discount=15),
            ... ]
            >>> response = client.prices.upload_prices(prices)
            >>> print(response.task_id)
        """
        payload = [p.model_dump(by_alias=True) for p in prices]
        data = self._post("/api/v2/upload/task", json=payload)
        return UploadTaskResponse(**data)

    def upload_size_prices(self, prices: list[SizePrice]) -> UploadTaskResponse:
        """
        Upload prices for specific product sizes.

        Args:
            prices: List of SizePrice objects

        Returns:
            UploadTaskResponse with task_id

        Example:
            >>> prices = [
            ...     SizePrice(size_id=123456, price=1500),
            ... ]
            >>> response = client.prices.upload_size_prices(prices)
        """
        payload = [p.model_dump(by_alias=True) for p in prices]
        data = self._post("/api/v2/upload/task/size", json=payload)
        return UploadTaskResponse(**data)

    def upload_club_discounts(
        self, discounts: list[ClubDiscount]
    ) -> UploadTaskResponse:
        """
        Upload WB Club member discounts.

        Args:
            discounts: List of ClubDiscount objects (0-50%)

        Returns:
            UploadTaskResponse with task_id

        Example:
            >>> discounts = [
            ...     ClubDiscount(nm_id=123456, club_discount=10),
            ... ]
            >>> response = client.prices.upload_club_discounts(discounts)
        """
        payload = [d.model_dump(by_alias=True) for d in discounts]
        data = self._post("/api/v2/upload/task/club-discount", json=payload)
        return UploadTaskResponse(**data)

    # === Task Monitoring ===

    def get_processed_tasks(
        self, limit: int = 10, offset: int = 0
    ) -> list[HistoryTask]:
        """
        Get history of processed tasks.

        Args:
            limit: Maximum number of tasks to return
            offset: Offset for pagination

        Returns:
            List of HistoryTask objects
        """
        params = {"limit": limit, "offset": offset}
        data = self._get("/api/v2/history/tasks", params=params)
        if not data or "tasks" not in data:
            return []
        return [HistoryTask(**task) for task in data["tasks"]]

    def get_task_details(self, task_id: str) -> PriceTaskDetails:
        """
        Get detailed information about processed task.

        Args:
            task_id: Task ID to check

        Returns:
            PriceTaskDetails with task status
        """
        params = {"taskId": task_id}
        data = self._get("/api/v2/history/goods/task", params=params)
        return PriceTaskDetails(**data)

    def get_pending_tasks(self) -> list[BufferTask]:
        """
        Get list of pending (unprocessed) tasks in queue.

        Returns:
            List of BufferTask objects
        """
        data = self._get("/api/v2/buffer/tasks")
        if not data or "tasks" not in data:
            return []
        return [BufferTask(**task) for task in data["tasks"]]

    def get_pending_task_details(self, task_id: str) -> PriceTaskDetails:
        """
        Get detailed information about pending task.

        Args:
            task_id: Task ID to check

        Returns:
            PriceTaskDetails with task status
        """
        params = {"taskId": task_id}
        data = self._get("/api/v2/buffer/goods/task", params=params)
        return PriceTaskDetails(**data)

    def wait_for_task(
        self,
        task_id: str,
        timeout: int = 300,
        interval: int = 2,
        on_progress: Callable[[PriceTaskDetails], None] | None = None,
    ) -> PriceTaskDetails:
        """
        Wait for price upload task to complete.

        Args:
            task_id: Task ID to monitor
            timeout: Maximum wait time in seconds
            interval: Initial polling interval in seconds
            on_progress: Optional callback for progress updates

        Returns:
            Completed PriceTaskDetails

        Raises:
            WBTaskTimeoutError: If timeout exceeded
            WBTaskFailedError: If task failed

        Example:
            >>> response = client.prices.upload_prices(prices)
            >>> def show_progress(task):
            ...     print(f"Progress: {task.progress_percent:.1f}%")
            >>> result = client.prices.wait_for_task(
            ...     response.task_id,
            ...     on_progress=show_progress
            ... )
            >>> print(f"Processed: {result.processed_items}")
        """
        return self._wait_for_task(
            task_id=task_id,
            check_fn=self.get_task_details,
            timeout=timeout,
            interval=interval,
            on_progress=on_progress,
        )

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
