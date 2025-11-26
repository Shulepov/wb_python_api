"""Common API for general operations."""

from typing import Any

from ..constants import DOMAINS
from .base import BaseAPI


class CommonAPI(BaseAPI):
    """API for common operations (ping, tariffs, news)."""

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
