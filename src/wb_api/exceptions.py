"""Exceptions for Wildberries API."""

from typing import Any


class WBAPIError(Exception):
    """Base exception for WB API errors."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response: dict[str, Any] | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class WBAuthError(WBAPIError):
    """Authentication error (401)."""

    pass


class WBForbiddenError(WBAPIError):
    """Access forbidden error (403)."""

    pass


class WBNotFoundError(WBAPIError):
    """Resource not found error (404)."""

    pass


class WBRateLimitError(WBAPIError):
    """Rate limit exceeded error (429)."""

    def __init__(
        self,
        message: str,
        retry_after: float | None = None,
        **kwargs: Any,
    ):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after

    def __str__(self) -> str:
        base = super().__str__()
        if self.retry_after:
            return f"{base} (retry after {self.retry_after}s)"
        return base


class WBValidationError(WBAPIError):
    """Request validation error (400)."""

    pass


class WBServerError(WBAPIError):
    """Server error (5xx)."""

    pass


class WBTimeoutError(WBAPIError):
    """Request timeout error."""

    pass


class WBConnectionError(WBAPIError):
    """Connection error."""

    pass


class WBTaskTimeoutError(WBAPIError):
    """Task execution timeout error."""

    def __init__(self, task_id: str, timeout: float):
        self.task_id = task_id
        self.timeout = timeout
        super().__init__(f"Task {task_id} timeout after {timeout:.1f}s")


class WBTaskFailedError(WBAPIError):
    """Task execution failed error."""

    def __init__(
        self,
        task_id: str,
        status: str,
        errors: list[dict[str, Any]] | None = None,
    ):
        self.task_id = task_id
        self.task_status = status
        self.task_errors = errors or []
        error_msg = f"Task {task_id} failed with status {status}"
        if errors:
            error_msg += f": {len(errors)} error(s)"
        super().__init__(error_msg, response={"errors": errors} if errors else None)
