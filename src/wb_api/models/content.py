"""Models for Content API (product cards)."""

from datetime import datetime
from typing import Any

from pydantic import Field

from .base import WBBaseModel


class Category(WBBaseModel):
    """Parent category."""

    id: int
    name: str
    is_visible: bool = Field(alias="isVisible")


class Subject(WBBaseModel):
    """Subject (subcategory)."""

    subject_id: int = Field(alias="subjectID")
    parent_id: int = Field(alias="parentID")
    subject_name: str = Field(alias="subjectName")
    parent_name: str = Field(alias="parentName")


class Characteristic(WBBaseModel):
    """Product characteristic."""

    charc_id: int = Field(alias="charcID")
    name: str
    required: bool = False
    unit_name: str = Field(alias="unitName", default="")
    max_count: int = Field(alias="maxCount", default=1)
    popular: bool = False
    charc_type: int = Field(alias="charcType", default=0)


class ProductSize(WBBaseModel):
    """Product size/variant."""

    chrt_id: int = Field(alias="chrtID")
    tech_size: str = Field(alias="techSize")
    skus: list[str] = []


class ProductDimensions(WBBaseModel):
    """Product dimensions."""

    length: int
    width: int
    height: int
    weight_brutto: float = Field(alias="weightBrutto")
    is_valid: bool = Field(alias="isValid", default=True)


class ProductPhoto(WBBaseModel):
    """Product photo."""

    big: str = ""
    medium: str = ""
    small: str = ""
    tm: str = ""


class ProductTag(WBBaseModel):
    """Product tag."""

    id: int
    name: str
    color: str


class ProductCharacteristic(WBBaseModel):
    """Product characteristic value."""

    id: int
    name: str
    value: list[str] = []


class ProductCard(WBBaseModel):
    """Product card."""

    nm_id: int = Field(alias="nmID")
    imt_id: int = Field(alias="imtID")
    nm_uuid: str = Field(alias="nmUUID")
    subject_id: int = Field(alias="subjectID")
    subject_name: str = Field(alias="subjectName")
    vendor_code: str = Field(alias="vendorCode")
    brand: str
    title: str
    description: str = ""
    photos: list[ProductPhoto] = []
    video: str = ""
    dimensions: ProductDimensions | None = None
    characteristics: list[ProductCharacteristic] = []
    sizes: list[ProductSize] = []
    tags: list[ProductTag] = []
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class Cursor(WBBaseModel):
    """Pagination cursor."""

    updated_at: str | None = Field(alias="updatedAt", default=None)
    nm_id: int | None = Field(alias="nmID", default=None)
    total: int = 0


class ProductCardsResponse(WBBaseModel):
    """Response with product cards list."""

    cards: list[ProductCard] = []
    cursor: Cursor


class CreateCardSize(WBBaseModel):
    """Size specification for card creation."""

    tech_size: str = Field(alias="techSize")
    wh_price: int | None = Field(alias="whPrice", default=None)
    skus: list[str] = []


class CreateCardCharacteristic(WBBaseModel):
    """Characteristic value for card creation."""

    id: int
    value: list[str] = []


class CreateCardVariant(WBBaseModel):
    """Product variant for card creation."""

    vendor_code: str = Field(alias="vendorCode")
    title: str
    description: str = ""
    brand: str
    dimensions: dict[str, Any]
    characteristics: list[CreateCardCharacteristic] = []
    sizes: list[CreateCardSize]


class CreateCardRequest(WBBaseModel):
    """Request for creating product card."""

    subject_id: int = Field(alias="subjectID")
    variants: list[CreateCardVariant]


class MediaFile(WBBaseModel):
    """Media file specification."""

    url: str


class UploadMediaRequest(WBBaseModel):
    """Request for uploading media files."""

    nm_id: int = Field(alias="nmId")
    data: list[str]


class Tag(WBBaseModel):
    """Tag."""

    id: int
    name: str
    color: str


class CreateTagRequest(WBBaseModel):
    """Request for creating tag."""

    name: str
    color: str = "D1CFD7"


class TrashRequest(WBBaseModel):
    """Request for moving cards to trash."""

    nm_ids: list[int] = Field(alias="nmIDs")
