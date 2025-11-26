"""Helper functions for WB API."""

from datetime import datetime
from typing import Any


def format_datetime(dt: datetime, fmt: str = "%Y-%m-%dT%H:%M:%S") -> str:
    """
    Format datetime to string.

    Args:
        dt: Datetime object
        fmt: Format string

    Returns:
        Formatted datetime string
    """
    return dt.strftime(fmt)


def parse_datetime(dt_str: str) -> datetime | None:
    """
    Parse datetime from string.

    Args:
        dt_str: Datetime string

    Returns:
        Datetime object or None if parsing fails
    """
    formats = [
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%d %H:%M:%S",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(dt_str, fmt)
        except ValueError:
            continue

    return None


def chunk_list(lst: list[Any], chunk_size: int) -> list[list[Any]]:
    """
    Split list into chunks.

    Args:
        lst: Input list
        chunk_size: Size of each chunk

    Returns:
        List of chunks
    """
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]
