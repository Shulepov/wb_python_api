"""Wildberries API Python SDK.

Python library for working with Wildberries API.

Example:
    >>> from wb_api import WildberriesClient
    >>>
    >>> client = WildberriesClient(token="your_api_token")
    >>>
    >>> # Get product cards
    >>> cards = client.content.get_cards(limit=10)
    >>> for card in cards.cards:
    ...     print(f"{card.nm_id}: {card.title}")
    >>>
    >>> # Use context manager
    >>> with WildberriesClient(token="token") as client:
    ...     cards = client.content.get_cards()
"""

from .auth import TokenDecoder, TokenInfo
from .client import WildberriesClient
from .config import WBConfig
from .exceptions import (
    WBAPIError,
    WBAuthError,
    WBConnectionError,
    WBForbiddenError,
    WBNotFoundError,
    WBRateLimitError,
    WBServerError,
    WBTaskFailedError,
    WBTaskTimeoutError,
    WBTimeoutError,
    WBValidationError,
)

__version__ = "0.1.0"

__all__ = [
    # Main client
    "WildberriesClient",
    # Configuration
    "WBConfig",
    # Authentication
    "TokenDecoder",
    "TokenInfo",
    # Exceptions
    "WBAPIError",
    "WBAuthError",
    "WBForbiddenError",
    "WBNotFoundError",
    "WBRateLimitError",
    "WBValidationError",
    "WBServerError",
    "WBTimeoutError",
    "WBConnectionError",
    "WBTaskTimeoutError",
    "WBTaskFailedError",
]
