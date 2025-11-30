"""Models for Seller Information API."""

from pydantic import Field

from .base import WBBaseModel


class SellerInfo(WBBaseModel):
    """
    Seller information model.

    Attributes:
        name: Seller's legal name (e.g., "ИП Кружинин В. Р.")
        sid: Unique seller account ID on Wildberries
        trade_mark: Seller's trade name (e.g., "Flax Store")
    """

    name: str = Field(description="Seller's legal name")
    sid: str = Field(description="Unique seller account ID (UUID)")
    trade_mark: str = Field(alias="tradeMark", description="Seller's trade name")
