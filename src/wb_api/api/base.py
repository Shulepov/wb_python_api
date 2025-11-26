"""Base class for all API modules."""

from typing import Any

import httpx

from ..exceptions import (
    WBAPIError,
    WBAuthError,
    WBConnectionError,
    WBForbiddenError,
    WBNotFoundError,
    WBRateLimitError,
    WBServerError,
    WBTimeoutError,
    WBValidationError,
)
from ..rate_limiter import RateLimiter


class BaseAPI:
    """Base class for all API modules."""

    domain: str = ""  # Must be overridden in subclasses

    def __init__(
        self,
        client: httpx.Client,
        token: str,
        rate_limiter: RateLimiter,
        sandbox: bool = False,
    ):
        """
        Initialize base API.

        Args:
            client: HTTPX client instance
            token: API token
            rate_limiter: Rate limiter instance
            sandbox: Use sandbox environment
        """
        self._client = client
        self._token = token
        self._rate_limiter = rate_limiter
        self._sandbox = sandbox

    @property
    def base_url(self) -> str:
        """Get base URL for this API."""
        return f"https://{self.domain}"

    def _headers(self, extra: dict[str, str] | None = None) -> dict[str, str]:
        """
        Get headers for API request.

        Args:
            extra: Additional headers to include

        Returns:
            Dictionary of headers
        """
        headers = {"Authorization": self._token}
        if extra:
            headers.update(extra)
        return headers

    def _request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json: Any | None = None,
        **kwargs: Any,
    ) -> Any:
        """
        Execute HTTP request with rate limiting and error handling.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            json: JSON body
            **kwargs: Additional arguments for httpx

        Returns:
            Response data (parsed JSON or None)

        Raises:
            WBAPIError: On API errors
            WBAuthError: On authentication errors
            WBRateLimitError: On rate limit exceeded
        """
        # Apply rate limiting
        self._rate_limiter.acquire()

        url = f"{self.base_url}{endpoint}"

        try:
            response = self._client.request(
                method=method,
                url=url,
                headers=self._headers(kwargs.pop("headers", None)),
                params=params,
                json=json,
                **kwargs,
            )
        except httpx.TimeoutException as e:
            raise WBTimeoutError(f"Request timeout: {e}")
        except httpx.ConnectError as e:
            raise WBConnectionError(f"Connection error: {e}")
        except httpx.HTTPError as e:
            raise WBAPIError(f"HTTP error: {e}")

        # Update rate limiter from response headers
        self._rate_limiter.update_from_headers(dict(response.headers))

        # Handle response
        self._handle_response(response)

        # Return None for 204 No Content
        if response.status_code == 204:
            return None

        # Try to parse JSON response
        try:
            return response.json()
        except Exception:
            # If response is not JSON, return text
            return response.text if response.text else None

    def _handle_response(self, response: httpx.Response) -> None:
        """
        Handle response and raise exceptions on errors.

        Args:
            response: HTTPX response object

        Raises:
            WBAPIError: On any API error
        """
        if response.is_success:
            return

        # Try to parse error response
        try:
            error_data = response.json()
        except Exception:
            error_data = {"detail": response.text}

        # Extract error message
        message = (
            error_data.get("detail")
            or error_data.get("message")
            or error_data.get("error")
            or str(error_data)
        )

        # Map status codes to exceptions
        if response.status_code == 400:
            raise WBValidationError(
                message, status_code=400, response=error_data
            )
        elif response.status_code == 401:
            raise WBAuthError(message, status_code=401, response=error_data)
        elif response.status_code == 403:
            raise WBForbiddenError(
                message, status_code=403, response=error_data
            )
        elif response.status_code == 404:
            raise WBNotFoundError(
                message, status_code=404, response=error_data
            )
        elif response.status_code == 429:
            retry_after = float(
                response.headers.get("x-ratelimit-retry", 1)
            )
            raise WBRateLimitError(
                message,
                status_code=429,
                response=error_data,
                retry_after=retry_after,
            )
        elif response.status_code >= 500:
            raise WBServerError(
                message,
                status_code=response.status_code,
                response=error_data,
            )
        else:
            raise WBAPIError(
                message,
                status_code=response.status_code,
                response=error_data,
            )

    def _get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        """Execute GET request."""
        return self._request("GET", endpoint, params=params, **kwargs)

    def _post(
        self, endpoint: str, json: Any | None = None, **kwargs: Any
    ) -> Any:
        """Execute POST request."""
        return self._request("POST", endpoint, json=json, **kwargs)

    def _put(
        self, endpoint: str, json: Any | None = None, **kwargs: Any
    ) -> Any:
        """Execute PUT request."""
        return self._request("PUT", endpoint, json=json, **kwargs)

    def _patch(
        self, endpoint: str, json: Any | None = None, **kwargs: Any
    ) -> Any:
        """Execute PATCH request."""
        return self._request("PATCH", endpoint, json=json, **kwargs)

    def _delete(self, endpoint: str, **kwargs: Any) -> Any:
        """Execute DELETE request."""
        return self._request("DELETE", endpoint, **kwargs)
