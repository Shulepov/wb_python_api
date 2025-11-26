"""Token authentication and decoding for Wildberries API."""

from dataclasses import dataclass
from datetime import datetime

import jwt


@dataclass
class TokenInfo:
    """Information extracted from WB API token."""

    token_id: str
    seller_id: str
    token_type: str  # "personal", "service", "base", "test"
    expires_at: datetime
    categories: list[str]
    is_read_only: bool


class TokenDecoder:
    """Decoder and validator for Wildberries JWT tokens."""

    # Bit positions for API categories in token permissions
    CATEGORY_BITS = {
        1: "content",
        2: "analytics",
        3: "prices",
        4: "marketplace",
        5: "statistics",
        6: "promotion",
        7: "feedbacks",
        9: "chat",
        10: "supplies",
        11: "returns",
        12: "documents",
        13: "finance",
    }

    @staticmethod
    def decode(token: str) -> TokenInfo:
        """
        Decode WB API token without signature verification.

        Args:
            token: JWT token string

        Returns:
            TokenInfo object with decoded token data

        Raises:
            jwt.DecodeError: If token is malformed
        """
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
        except jwt.DecodeError as e:
            raise ValueError(f"Invalid token format: {e}")

        # Determine token type based on 'acc' field
        acc = payload.get("acc")
        if acc == 1:
            token_type = "base"
        elif acc == 2:
            token_type = "test"
        elif acc == 3:
            token_type = "personal"
        elif acc == 4:
            token_type = "service"
        else:
            token_type = "unknown"

        # Parse categories from bit mask
        s = payload.get("s", 0)
        categories = []
        for bit, category in TokenDecoder.CATEGORY_BITS.items():
            if s & (1 << bit):
                categories.append(category)

        # Check if token is read-only (bit 30)
        is_read_only = bool(s & (1 << 30))

        # Parse expiration time
        exp = payload.get("exp", 0)
        expires_at = datetime.fromtimestamp(exp) if exp else datetime.now()

        return TokenInfo(
            token_id=payload.get("id", ""),
            seller_id=payload.get("sid", ""),
            token_type=token_type,
            expires_at=expires_at,
            categories=categories,
            is_read_only=is_read_only,
        )

    @staticmethod
    def is_expired(token: str) -> bool:
        """
        Check if token has expired.

        Args:
            token: JWT token string

        Returns:
            True if token is expired, False otherwise
        """
        try:
            info = TokenDecoder.decode(token)
            return datetime.now() > info.expires_at
        except (jwt.DecodeError, ValueError):
            return True

    @staticmethod
    def has_category_access(token: str, category: str) -> bool:
        """
        Check if token has access to a specific category.

        Args:
            token: JWT token string
            category: Category name (e.g., "content", "prices")

        Returns:
            True if token has access to category, False otherwise
        """
        try:
            info = TokenDecoder.decode(token)
            return category in info.categories
        except (jwt.DecodeError, ValueError):
            return False

    @staticmethod
    def validate_token(token: str, category: str | None = None) -> tuple[bool, str | None]:
        """
        Validate token and optionally check category access.

        Args:
            token: JWT token string
            category: Optional category name to check access for

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            info = TokenDecoder.decode(token)
        except (jwt.DecodeError, ValueError) as e:
            return False, f"Invalid token: {e}"

        # Check if expired
        if datetime.now() > info.expires_at:
            return False, "Token has expired"

        # Check category access if specified
        if category and category not in info.categories:
            return False, f"Token does not have access to '{category}' category"

        return True, None
