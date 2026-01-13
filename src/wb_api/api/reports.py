"""Reports API - comprehensive reporting and analytics."""

from datetime import date, datetime
import time
from ..constants import DOMAINS, SANDBOX_DOMAINS
from ..models.reports import (
    MeasurementTab,
    ParentSubject,
    ReportTaskResponse,
    ReportTaskStatus,
)

from .base import BaseAPI


class ReportsAPI(BaseAPI):
    """API for reports and analytics."""

    @property
    def domain(self) -> str:
        """Get API domain."""
        # Reports API uses statistics domain
        if self._sandbox:
            return SANDBOX_DOMAINS.get("analytics", DOMAINS["statistics"])
        return DOMAINS["analytics"]

    # === Excise Report ===

    def get_excise_report(
        self, date_from: date | datetime, date_to: date | datetime
    ) -> list[dict]:
        """Get excise (marking) report.

        Args:
            date_from: Start date.
            date_to: End date.

        Returns:
            List of ExciseReportItem objects.

        Rate limit: 10 requests per 5 hours
        """
        if isinstance(date_from, datetime):
            date_from = date_from.date()
        if isinstance(date_to, datetime):
            date_to = date_to.date()

        payload = {
            "dateFrom": date_from.isoformat(),
            "dateTo": date_to.isoformat(),
        }

        data = self._post("/api/v1/analytics/excise-report", json=payload)
        return data.get("data", [])

    # === Deduction Reports ===

    def get_warehouse_measurements(
        self,
        date_from: date | datetime | None,
        date_to: date | datetime,
        tab: MeasurementTab,
        limit: int = 1000,
        offset: int = 0,
    ) -> list[dict]:
        """Get warehouse measurements (size penalties) report.

        Args:
            date_from: Start date. Optional
            date_to: End date.
            limit: limit of results, max 1000
            offset: results offset

        Returns:
            List of WarehouseMeasurement objects.

        Rate limit: 5 requests/minute
        """
        from datetime import datetime, date, time, timezone  # , timedelta

        # gmt3 = timezone(timedelta(hours=3))
        if (
            date_from
            and isinstance(date_from, date)
            and not isinstance(date_from, datetime)
        ):
            date_from = datetime.combine(date_from, time(0, 0, 0), tzinfo=timezone.utc)
        if isinstance(date_to, date) and not isinstance(date_to, datetime):
            date_to = datetime.combine(date_to, time(23, 59, 59), tzinfo=timezone.utc)

        params = {
            "dateTo": date_to.isoformat(),
            "tab": tab.value,
            "limit": limit,
            "offset": offset,
        }

        if date_from:
            params["dateFrom"] = date_from.isoformat()

        data = self._get("/api/v1/analytics/warehouse-measurements", params=params)
        return data.get("data", {}).get("reports", [])

    def get_antifraud_details(
        self,
        date_from: date | datetime | None,
    ) -> list[dict]:
        """Get antifraud (self-redemption) details report.
        Data is available from August 2023

        Args:
            date: Start date.

        Returns:
            List of AntifraudDetail objects.

        Rate limit: 1 requests per 10 minutes
        """
        if date_from and isinstance(date_from, datetime):
            date_from = date_from.date()

        params = {}
        if date_from:
            params["date"] = date_from.isoformat()

        data = self._get("/api/v1/analytics/antifraud-details", params=params)
        return data.get("details", [])

    def get_incorrect_attachments(
        self,
        date_from: date | datetime,
        date_to: date | datetime,
    ) -> list[dict]:
        """Get incorrect attachments (product substitution) report.

        Args:
            date_from: Start date.
            date_to: End date. Max 31 days range

        Returns:
            List of IncorrectAttachment objects.

        Rate limit: 1 request/minute (burst 10)
        """
        if isinstance(date_from, datetime):
            date_from = date_from.date()
        if isinstance(date_to, datetime):
            date_to = date_to.date()

        params = {
            "dateFrom": date_from.isoformat(),
            "dateTo": date_to.isoformat(),
        }

        data = self._get("/api/v1/analytics/incorrect-attachments", params=params)
        return data.get("report", [])

    def get_goods_labeling(
        self,
        date_from: date | datetime,
        date_to: date | datetime,
    ) -> list[dict]:
        """Get goods labeling penalties report.
        Data available from March 2024
        Args:
            date_from: Start date.
            date_to: End date. Max 31 days range

        Returns:
            List of GoodsLabeling objects.

        Rate limit: 10 requests per 10 minutes
        """
        if isinstance(date_from, datetime):
            date_from = date_from.date()
        if isinstance(date_to, datetime):
            date_to = date_to.date()

        params = {
            "dateFrom": date_from.isoformat(),
            "dateTo": date_to.isoformat(),
        }

        data = self._get("/api/v1/analytics/goods-labeling", params=params)
        return data.get("report", [])

    def get_characteristics_change(
        self,
        date_from: date | datetime,
        date_to: date | datetime,
    ) -> list[dict]:
        """Get characteristics change penalties report.
        Data available from 28 Dec 2021
        Args:
            date_from: Start date.
            date_to: End date. Max 31 days range

        Returns:
            List of CharacteristicsChange objects.

        Rate limit: 10 requests per 10 minutes
        """
        if isinstance(date_from, datetime):
            date_from = date_from.date()
        if isinstance(date_to, datetime):
            date_to = date_to.date()

        params = {
            "dateFrom": date_from.isoformat(),
            "dateTo": date_to.isoformat(),
        }

        data = self._get("/api/v1/analytics/characteristics-change", params=params)
        return data.get("report", [])

    # === Region Sales ===

    def get_region_sales(
        self,
        date_from: date | datetime,
        date_to: date | datetime,
    ) -> list[dict]:
        """Get region sales report.

        Args:
            date_from: Start date.
            date_to: End date. Max 31 days range

        Returns:
            List of RegionSale objects.

        Rate limit: 1 request per 10 seconds (burst 5)
        """
        if isinstance(date_from, datetime):
            date_from = date_from.date()
        if isinstance(date_to, datetime):
            date_to = date_to.date()

        params = {
            "dateFrom": date_from.isoformat(),
            "dateTo": date_to.isoformat(),
        }

        data = self._get("/api/v1/analytics/region-sale", params=params)
        return data.get("report", [])

    # === Brand Share ===

    def get_brand_list(self) -> list[str]:
        """Get list of seller's brands.

        Returns:
            List of Brand objects.

        Rate limit: 1 request/minute (burst 10)
        """
        data = self._get("/api/v1/analytics/brand-share/brands")
        return data

    def get_parent_subjects(
        self, brand: str, date_from: date, date_to: date
    ) -> list[ParentSubject]:
        """Get parent subjects (categories) for brand.

        Args:
            brand: Brand name.
            date_from: date start. Min 1 Nov 2022
            date_to: date end. max 365 days range

        Returns:
            List of ParentSubject objects.

        Rate limit: 1 request/minute (burst 10)
        """
        params = {
            "brand": brand,
            "dateFrom": date_from.isoformat(),
            "dateTo": date_to.isoformat(),
        }
        data = self._get("/api/v1/analytics/brand-share/parent-subjects", params=params)
        data = data.get("data", [])
        return [ParentSubject(**item) for item in data]

    def get_brand_share(
        self,
        parent_id: int,
        brand: str,
        date_from: date | datetime,
        date_to: date | datetime,
    ) -> list[dict]:
        """Get brand share report.

        Args:
            parent_id: Parent id
            brand: Brand name.
            date_from: Start date. Min - 1 Nov 2022
            date_to: End date. Max 365 days range

        Returns:
            List of BrandShare objects.

        Rate limit: 1 request/minute (burst 10)
        """
        if isinstance(date_from, datetime):
            date_from = date_from.date()
        if isinstance(date_to, datetime):
            date_to = date_to.date()

        params = {
            "parentId": parent_id,
            "brand": brand,
            "dateFrom": date_from.isoformat(),
            "dateTo": date_to.isoformat(),
        }

        data = self._get("/api/v1/analytics/brand-share", params=params)
        return data.get("report", [])

    # === Generated Reports (with tasks) ===

    def create_warehouse_remains(self) -> ReportTaskResponse:
        """Create warehouse remains report task.

        Returns:
            ReportTaskResponse with task_id.

        Rate limit: 1 request/minute (burst 5)
        """
        data = self._get("/api/v1/warehouse_remains")
        return ReportTaskResponse(**data)

    def check_warehouse_remains_status(self, task_id: str) -> ReportTaskStatus:
        """Check warehouse remains report task status.

        Args:
            task_id: Task ID from create_warehouse_remains.

        Returns:
            ReportTaskStatus object.

        Rate limit: 1 request per 5 seconds (burst 5)
        """
        data = self._get(f"/api/v1/warehouse_remains/tasks/{task_id}/status")
        return ReportTaskStatus(**data)

    def download_warehouse_remains(self, task_id: str) -> list[dict]:
        """Download warehouse remains report.

        Args:
            task_id: Task ID from create_warehouse_remains.

        Returns:
            Report file content (Excel/CSV).

        Rate limit: 1 request/minute
        """
        data = self._get(f"/api/v1/warehouse_remains/tasks/{task_id}/download")
        return data

    def create_acceptance_report(
        self, date_from: date | datetime, date_to: date | datetime
    ) -> ReportTaskResponse:
        """Create acceptance report task.

        Returns:
            ReportTaskResponse with task_id.

        Rate limit: 1 request/minute
        """
        if isinstance(date_from, datetime):
            date_from = date_from.date()
        if isinstance(date_to, datetime):
            date_to = date_to.date()

        data = self._get(
            "/api/v1/acceptance_report",
            params={"dateFrom": date_from.isoformat(), "dateTo": date_to.isoformat()},
        )
        return ReportTaskResponse(**data)

    def check_acceptance_status(self, task_id: str) -> ReportTaskStatus:
        """Check acceptance report task status.

        Args:
            task_id: Task ID from create_acceptance_report.

        Returns:
            ReportTaskStatus object.

        Rate limit: 1 request per 5 seconds
        """
        data = self._get(f"/api/v1/acceptance_report/tasks/{task_id}/status")
        return ReportTaskStatus(**data)

    def download_acceptance_report(self, task_id: str) -> list[dict]:
        """Download acceptance report.

        Args:
            task_id: Task ID from create_acceptance_report.

        Returns:
            Json array

        Rate limit: 1 request/minute
        """
        data = self._get(f"/api/v1/acceptance_report/tasks/{task_id}/download")
        return data

    def create_paid_storage(
        self, date_from: date | datetime, date_to: date | datetime
    ) -> ReportTaskResponse:
        """Create paid storage report task.

        Returns:
            ReportTaskResponse with task_id.

        Rate limit: 1 request/minute (burst 5)
        """
        if isinstance(date_from, datetime):
            date_from = date_from.date()
        if isinstance(date_to, datetime):
            date_to = date_to.date()

        data = self._get(
            "/api/v1/paid_storage",
            params={"dateFrom": date_from.isoformat(), "dateTo": date_to.isoformat()},
        )
        return ReportTaskResponse(**data)

    def check_paid_storage_status(self, task_id: str) -> ReportTaskStatus:
        """Check paid storage report task status.

        Args:
            task_id: Task ID from create_paid_storage.

        Returns:
            ReportTaskStatus object.

        Rate limit: 1 request per 5 seconds (burst 5)
        """
        data = self._get(f"/api/v1/paid_storage/tasks/{task_id}/status")
        return ReportTaskStatus(**data)

    def download_paid_storage(self, task_id: str) -> list[dict]:
        """Download paid storage report.

        Args:
            task_id: Task ID from create_paid_storage.

        Returns:
            JSON.

        Rate limit: 1 request/minute
        """
        data = self._get(f"/api/v1/paid_storage/tasks/{task_id}/download")
        return data

    # === Helper methods for generated reports ===

    def _wait_for_task(
        self, task_id: str, check_fn, timeout: int, interval: int
    ) -> str:
        """
        Ждать завершения задачи с периодической проверкой статуса

        Args:
            task_id: ID задачи для ожидания
            check_fn: Функция проверки статуса (self, task_id) -> ReportTaskStatus
            timeout: Максимальное время ожидания в секундах
            interval: Интервал между проверками в секундах

        Returns:
            ReportTaskStatus: Финальный статус задачи

        Raises:
            TimeoutError: Если задача не завершилась за timeout секунд
        """
        start_time = time.time()

        while True:
            # Проверить текущий статус
            status = check_fn(task_id)

            # Если задача завершена - вернуть статус
            if status.is_completed:
                elapsed = time.time() - start_time
                # logger.info(f"Task {task_id} completed in {elapsed:.1f}s")
                return status

            # Проверить timeout
            elapsed = time.time() - start_time
            if elapsed >= timeout:
                raise TimeoutError(
                    f"Task {task_id} did not complete within {timeout}s. "
                    f"Last status: {status}"
                )

            # Подождать перед следующей проверкой (не превышая timeout)
            remaining = timeout - elapsed
            sleep_time = min(interval, remaining)

            if sleep_time > 0:
                time.sleep(sleep_time)

    def wait_for_warehouse_remains(
        self,
        task_id: str,
        timeout: int = 300,
        interval: float = 10.0,
    ) -> ReportTaskStatus:
        """Wait for warehouse remains report to complete.

        Args:
            task_id: Task ID.
            timeout: Maximum wait time in seconds.
            interval: Check interval in seconds.

        Returns:
            ReportTaskStatus when completed.
        """
        return self._wait_for_task(
            task_id=task_id,
            check_fn=self.check_warehouse_remains_status,
            timeout=timeout,
            interval=interval,
        )

    def wait_for_acceptance_report(
        self,
        task_id: str,
        timeout: int = 300,
        interval: float = 10.0,
    ) -> ReportTaskStatus:
        """Wait for acceptance report to complete.

        Args:
            task_id: Task ID.
            timeout: Maximum wait time in seconds.
            interval: Check interval in seconds.

        Returns:
            ReportTaskStatus when completed.
        """
        return self._wait_for_task(
            task_id=task_id,
            check_fn=self.check_acceptance_status,
            timeout=timeout,
            interval=interval,
        )

    def wait_for_paid_storage(
        self,
        task_id: str,
        timeout: int = 300,
        interval: float = 10.0,
    ) -> ReportTaskStatus:
        """Wait for paid storage report to complete.

        Args:
            task_id: Task ID.
            timeout: Maximum wait time in seconds.
            interval: Check interval in seconds.

        Returns:
            ReportTaskStatus when completed.
        """
        return self._wait_for_task(
            task_id=task_id,
            check_fn=self.check_paid_storage_status,
            timeout=timeout,
            interval=interval,
        )
