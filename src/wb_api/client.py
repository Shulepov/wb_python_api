"""Main Wildberries API client."""


import httpx

from .api.common import CommonAPI
from .api.content import ContentAPI
from .api.finance import FinanceAPI
from .api.marketing import MarketingAPI
from .api.prices import PricesAPI
from .api.promotions import PromotionsAPI
from .api.reports import ReportsAPI
from .api.statistics import StatisticsAPI
from .auth import TokenDecoder, TokenInfo
from .config import WBConfig
from .constants import DEFAULT_RATE_LIMITS
from .rate_limiter import RateLimiter


class WildberriesClient:
    """Main client for working with Wildberries API."""

    def __init__(
        self,
        token: str,
        sandbox: bool = False,
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        """
        Initialize Wildberries API client.

        Args:
            token: API token
            sandbox: Use sandbox environment
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries on failure

        Example:
            >>> client = WildberriesClient(token="your_token")
            >>> cards = client.content.get_cards(limit=10)
        """
        self._token = token
        self._sandbox = sandbox
        self._config = WBConfig(
            token=token,
            sandbox=sandbox,
            timeout=timeout,
            max_retries=max_retries,
        )

        # Create HTTP client
        self._client = httpx.Client(
            timeout=timeout,
            follow_redirects=True,
        )

        # Create rate limiters for each category
        self._rate_limiters = {
            name: RateLimiter(limits["rpm"], limits["burst"])
            for name, limits in DEFAULT_RATE_LIMITS.items()
        }

        # Initialize API modules
        self._init_api_modules()

    def _init_api_modules(self) -> None:
        """Initialize all API modules."""
        self.content = ContentAPI(
            self._client,
            self._token,
            self._rate_limiters.get("content", RateLimiter(100, 5)),
            self._sandbox,
        )

        self.prices = PricesAPI(
            self._client,
            self._token,
            self._rate_limiters.get("prices", RateLimiter(100, 5)),
            self._sandbox,
        )

        self.finance = FinanceAPI(
            self._client,
            self._token,
            self._rate_limiters.get("finance", RateLimiter(1, 1)),
            self._sandbox,
        )

        self.statistics = StatisticsAPI(
            self._client,
            self._token,
            self._rate_limiters.get("statistics", RateLimiter(1, 1)),
            self._sandbox,
        )

        self.common = CommonAPI(
            self._client,
            self._token,
            self._rate_limiters.get("common", RateLimiter(60, 10)),
            self._sandbox,
        )

        self.marketing = MarketingAPI(
            self._client,
            self._token,
            self._rate_limiters.get("promotion", RateLimiter(60, 10)),
            self._sandbox,
        )

        self.promotions = PromotionsAPI(
            self._client,
            self._token,
            self._rate_limiters.get("promotion", RateLimiter(60, 10)),
            self._sandbox,
        )

        self.reports = ReportsAPI(
            self._client,
            self._token,
            self._rate_limiters.get("statistics", RateLimiter(1, 1)),
            self._sandbox,
        )

    @property
    def token_info(self) -> TokenInfo:
        """
        Get information about the current token.

        Returns:
            TokenInfo object with token details
        """
        return TokenDecoder.decode(self._token)

    def validate_token(self) -> tuple[bool, str | None]:
        """
        Validate the current token.

        Returns:
            Tuple of (is_valid, error_message)
        """
        return TokenDecoder.validate_token(self._token)

    def ping(self) -> dict:
        """
        Check API connection.

        Returns:
            Response data from ping endpoint
        """
        return self.common.ping()

    def __enter__(self) -> "WildberriesClient":
        """Context manager entry."""
        return self

    def __exit__(self, *args) -> None:
        """Context manager exit."""
        self.close()

    def close(self) -> None:
        """Close HTTP client and cleanup resources."""
        self._client.close()

    def __repr__(self) -> str:
        """String representation of the client."""
        try:
            info = self.token_info
            return (
                f"WildberriesClient("
                f"seller_id={info.seller_id}, "
                f"token_type={info.token_type}, "
                f"sandbox={self._sandbox})"
            )
        except Exception:
            return f"WildberriesClient(sandbox={self._sandbox})"
