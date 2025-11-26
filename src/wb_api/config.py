"""Configuration module for WB API client."""

from dataclasses import dataclass


@dataclass
class WBConfig:
    """Configuration for Wildberries API client."""

    token: str
    sandbox: bool = False
    timeout: float = 30.0
    max_retries: int = 3
    retry_delay: float = 1.0

    def __post_init__(self):
        """Validate configuration after initialization."""
        if not self.token:
            raise ValueError("Token cannot be empty")
        if self.timeout <= 0:
            raise ValueError("Timeout must be positive")
        if self.max_retries < 0:
            raise ValueError("Max retries cannot be negative")
        if self.retry_delay < 0:
            raise ValueError("Retry delay cannot be negative")
