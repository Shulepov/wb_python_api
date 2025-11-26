"""Finance API for seller balance information."""

from ..constants import DOMAINS
from ..models.finance import Balance
from .base import BaseAPI


class FinanceAPI(BaseAPI):
    """API for working with seller balance."""

    @property
    def domain(self) -> str:
        """Get domain for Finance API."""
        return DOMAINS["finance"]

    def get_balance(self) -> Balance:
        """
        Get current seller balance.

        Returns:
            Balance object with current and withdrawable amounts

        Rate Limit:
            1 request per minute

        Example:
            >>> balance = client.finance.get_balance()
            >>> print(f"Current: {balance.current}₽")
            >>> print(f"Available: {balance.for_withdraw}₽")
            >>> print(f"Blocked: {balance.blocked}₽ ({balance.blocked_percent:.1f}%)")
        """
        data = self._get("/api/v1/account/balance")
        return Balance(**data)
