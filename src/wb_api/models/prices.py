"""Models for Prices API (prices and discounts)."""

from datetime import datetime

from pydantic import Field

from .base import WBBaseModel

# === Price Models ===


class Price(WBBaseModel):
    """Price and discount for product."""

    nm_id: int = Field(alias="nmID")
    price: int  # Price in rubles
    discount: int = 0  # Discount in percent (0-99)


class SizeUpdatePrice(WBBaseModel):
    """Price for specific product size. Used for uploading price data."""

    nm_id: int = Field(alias="nmID")
    size_id: int = Field(alias="sizeID")  # chrtID
    price: int  # Price in rubles


class ClubDiscount(WBBaseModel):
    """WB Club member discount."""

    nm_id: int = Field(alias="nmID")
    club_discount: int = Field(alias="clubDiscount")  # 0-50%


# === Request Models ===

class FilterGoodsRequest(WBBaseModel):
    """Request for filtering goods by vendor codes."""

    vendor_codes: list[str] = Field(alias="vendorCodes")


# === Response Models ===


class SizePrice(WBBaseModel):
    """Size with price information."""

    size_id: int = Field(alias="sizeID") # chrt_id in GoodSize
    price: int = Field(alias="price")
    discounted_price: float = Field(alias="discountedPrice")
    club_discounted_price: float = Field(alias="clubDiscountedPrice")
    tech_size_name: str = Field(alias="techSizeName")

class GoodPrice(WBBaseModel):
    """Product with price information."""

    nm_id: int = Field(alias="nmID")
    vendor_code: str = Field(alias="vendorCode")
    sizes: list[SizePrice] = []  # Size information
    discount: int
    club_discount: int = Field(alias="clubDiscount", default=0)
    editable_size_price: bool = Field(alias="editableSizePrice", default=False)
    is_bad_turnover: bool = Field(alias="isBadTurnover", default=False)


class GoodSize(WBBaseModel):
    """Product size with price."""

    size_id: int = Field(alias="sizeID")
    nm_id: int = Field(alias="nmID")
    chrt_id: int = Field(alias="chrtID")
    tech_size: str = Field(alias="techSize")
    wh_price: int = Field(alias="whPrice", default=0)
    price: int
    discount: int = 0


class QuarantineGood(WBBaseModel):
    """Product in quarantine (price issues)."""

    nm_id: int = Field(alias="nmID")
    vendor_code: str = Field(alias="vendorCode")
    reason: str
    quarantine_date: datetime | None = Field(alias="quarantineDate", default=None)

