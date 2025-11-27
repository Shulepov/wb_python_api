"""Models for Promotions API (Promotions Calendar)."""

from datetime import date, datetime

from pydantic import Field

from .base import WBBaseModel


class Promotion(WBBaseModel):
    """Promotion information from calendar."""

    promotion_id: int = Field(alias="id")
    name: str
    description: str | None = None
    start_date: date = Field(alias="startDateTime")
    end_date: date = Field(alias="endDateTime")

    # Additional fields
    type: str | None = None
    is_active: bool = Field(alias="isActive", default=False)


class PromotionDetails(WBBaseModel):
    """Detailed promotion information."""

    promotion_id: int = Field(alias="id")
    name: str
    description: str | None = None
    start_date: datetime = Field(alias="startDateTime")
    end_date: datetime = Field(alias="endDateTime")

    # Detailed fields
    type: str
    mechanic: str | None = None  # Promotion mechanic
    discount_type: str | None = Field(alias="discountType", default=None)
    discount_value: float | None = Field(alias="discountValue", default=None)

    # Participation conditions
    min_price: float | None = Field(alias="minPrice", default=None)
    max_price: float | None = Field(alias="maxPrice", default=None)
    categories: list[str] = Field(default_factory=list)

    # Status
    is_active: bool = Field(alias="isActive", default=False)
    is_available: bool = Field(alias="isAvailable", default=False)


class PromotionItem(WBBaseModel):
    """Item available for promotion."""

    nm_id: int = Field(alias="nmID")
    vendor_code: str = Field(alias="vendorCode")
    title: str
    brand: str | None = None
    subject: str | None = None

    # Price information
    price: float
    discount: float = 0.0
    promo_price: float | None = Field(alias="promoPrice", default=None)

    # Participation status
    is_participating: bool = Field(alias="isParticipating", default=False)
    is_available: bool = Field(alias="isAvailable", default=True)

    # Stock information
    stock: int = 0
    in_way_to_client: int = Field(alias="inWayToClient", default=0)
    in_way_from_client: int = Field(alias="inWayFromClient", default=0)
