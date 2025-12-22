"""Statistics API for sales reports and analytics."""

from collections.abc import Iterator
from datetime import datetime, date, timedelta
from typing import Any

from ..constants import DOMAINS, SANDBOX_DOMAINS
from ..models.statistics import (
    ReportPeriod,
    SalesReportItem,
    Income,
    Order,
    Stock,
    Sale,
)
from .base import BaseAPI


class StatisticsAPI(BaseAPI):
    """API for sales statistics and reports."""

    @property
    def domain(self) -> str:
        """Get domain for Statistics API."""
        if self._sandbox:
            return SANDBOX_DOMAINS.get("statistics", DOMAINS["statistics"])
        return DOMAINS["statistics"]

    # === Basic Reports ===

    def get_incomes(self, date_from: date | datetime) -> list[Income]:
        """Get incomes (supplies) report.

        Args:
            date_from: Start date for report.

        Returns:
            List of Income objects.

        Rate limit: 1 request/minute
        """
        if isinstance(date_from, datetime):
            date_from = date_from.date()

        params = {"dateFrom": date_from.isoformat()}
        data = self._get("/api/v1/supplier/incomes", params=params)
        return [Income(**item) for item in data]

    def get_stocks(self, date_from: date | datetime) -> list[Stock]:
        """Get stocks (warehouse remains) report.

        Args:
            date_from: Start date for report.

        Returns:
            List of Stock objects.

        Rate limit: 1 request/minute
        """
        if isinstance(date_from, datetime):
            date_from = date_from.date()

        params = {"dateFrom": date_from.isoformat()}
        data = self._get("/api/v1/supplier/stocks", params=params)
        return [Stock(**item) for item in data]

    def get_orders(self, date_from: date | datetime, flag: int = 0) -> list[Order]:
        """Get orders report.

        Args:
            date_from: Start date for report.
            flag: 0 - new orders since date_from, 1 - orders updated since date_from.

        Returns:
            List of Order objects.

        Rate limit: 1 request/minute
        """
        if isinstance(date_from, datetime):
            date_from = date_from.date()

        params = {"dateFrom": date_from.isoformat(), "flag": flag}
        data = self._get("/api/v1/supplier/orders", params=params)
        return [Order(**item) for item in data]

    def get_sales(self, date_from: date | datetime, flag: int = 0) -> list[Sale]:
        """Get sales report.

        Args:
            date_from: Start date for report.
            flag: 0 - new sales since date_from, 1 - sales updated since date_from.

        Returns:
            List of Sale objects.

        Rate limit: 1 request/minute
        """
        if isinstance(date_from, datetime):
            date_from = date_from.date()

        params = {"dateFrom": date_from.isoformat(), "flag": flag}
        data = self._get("/api/v1/supplier/sales", params=params)
        return [Sale(**item) for item in data]

    def get_sales_report(
        self,
        date_from: str | datetime,
        date_to: str | datetime,
        limit: int = 100000,
        rrd_id: int = 0,
        period: ReportPeriod | str = ReportPeriod.WEEKLY,
    ) -> list[SalesReportItem]:
        """
        Get detailed sales report by period.

        Args:
            date_from: Start date (RFC3339 format or datetime)
            date_to: End date (RFC3339 format or datetime)
            limit: Maximum rows to return (max 100,000)
            rrd_id: Row ID for pagination (use last item's rrd_id)
            period: Report period ("daily" or "weekly")

        Returns:
            List of SalesReportItem objects

        Rate Limit:
            1 request per minute

        Note:
            Data available from January 29, 2024

        Example:
            >>> from datetime import datetime, timedelta
            >>>
            >>> date_to = datetime.now()
            >>> date_from = date_to - timedelta(days=7)
            >>>
            >>> report = client.statistics.get_sales_report(
            ...     date_from=date_from,
            ...     date_to=date_to,
            ...     period="daily"
            ... )
            >>>
            >>> total = sum(item.ppvz_for_pay for item in report)
            >>> print(f"Total to seller: {total}₽")
        """
        # Format dates
        if isinstance(date_from, datetime):
            date_from = date_from.strftime("%Y-%m-%d")
        if isinstance(date_to, datetime):
            date_to = date_to.strftime("%Y-%m-%d")

        params: dict[str, Any] = {
            "dateFrom": date_from,
            "dateTo": date_to,
            "limit": min(limit, 100000),
            "rrdid": rrd_id,
        }

        if period:
            params["period"] = (
                period.value if isinstance(period, ReportPeriod) else period
            )

        data = self._get("/api/v5/supplier/reportDetailByPeriod", params=params)
        if not data:
            return []
        return [SalesReportItem(**item) for item in data]

    def iter_sales_report(
        self,
        date_from: str | datetime,
        date_to: str | datetime,
        batch_size: int = 100000,
        period: ReportPeriod | str = ReportPeriod.WEEKLY,
    ) -> Iterator[SalesReportItem]:
        """
        Iterate over full sales report with automatic pagination.

        Args:
            date_from: Start date
            date_to: End date
            batch_size: Records per request (max 100,000)
            period: Report period

        Yields:
            SalesReportItem objects

        Example:
            >>> for item in client.statistics.iter_sales_report(
            ...     date_from="2024-01-01",
            ...     date_to="2024-01-31"
            ... ):
            ...     print(f"{item.nm_id}: {item.ppvz_for_pay}₽")
        """
        rrd_id = 0
        batch_size = min(batch_size, 100000)

        while True:
            items = self.get_sales_report(
                date_from=date_from,
                date_to=date_to,
                limit=batch_size,
                rrd_id=rrd_id,
                period=period,
            )

            if not items:
                break

            yield from items

            if len(items) < batch_size:
                break

            # Update rrd_id for next page
            rrd_id = items[-1].rrd_id

    def get_last_completed_week_dates() -> tuple[date, date]:
        """
        Возвращает даты прошлой завершенной недели (пн-вс)

        WB генерирует отчет за неделю в понедельник следующей недели.
        Поэтому "прошлая завершенная неделя" - это неделя, которая
        закончилась в прошлое воскресенье.
        """
        today = datetime.now().date()

        # Понедельник прошлой недели
        date_from = today - timedelta(days=today.weekday() + 7)

        # Воскресенье прошлой недели
        date_to = date_from + timedelta(days=6)

        return date_from, date_to
