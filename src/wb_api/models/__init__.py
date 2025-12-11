"""Pydantic models for Wildberries API."""

from .base import (
    WBBaseModel,
)
from .seller_info import SellerInfo

__all__ = [
    "WBBaseModel",
    "SellerInfo",
]
