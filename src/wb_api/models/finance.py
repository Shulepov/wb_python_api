"""Models for Finance API (seller balance)."""

from pydantic import Field

from .base import WBBaseModel


class Balance(WBBaseModel):
    """Seller balance information."""

    currency: str  # Currency code (e.g., "RUB")
    current: float  # Current balance amount
    for_withdraw: float = Field(alias="forWithdraw")  # Available for withdrawal

    @property
    def blocked(self) -> float:
        """Calculate blocked (unavailable) amount."""
        return self.current - self.for_withdraw

    @property
    def blocked_percent(self) -> float:
        """Calculate percentage of blocked funds."""
        if self.current == 0:
            return 0.0
        return (self.blocked / self.current) * 100
