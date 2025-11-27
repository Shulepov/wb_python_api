"""Models for Reports API."""

from datetime import date, datetime

from pydantic import Field

from .base import WBBaseModel

# === Basic Reports ===


class Income(WBBaseModel):
    """Income (supply) report item."""

    income_id: int = Field(alias="incomeId")
    number: str  # Supply number
    date: datetime  # Supply date
    last_change_date: datetime = Field(alias="lastChangeDate")
    supplier_article: str = Field(alias="supplierArticle")
    tech_size: str = Field(alias="techSize")
    barcode: str
    quantity: int
    total_price: float = Field(alias="totalPrice")
    date_close: datetime = Field(alias="dateClose")
    warehouse_name: str = Field(alias="warehouseName")
    nm_id: int = Field(alias="nmId")
    status: str  # Supply status


class Stock(WBBaseModel):
    """Stock (warehouse remains) report item."""

    last_change_date: datetime = Field(alias="lastChangeDate")
    supplier_article: str = Field(alias="supplierArticle")
    tech_size: str = Field(alias="techSize")
    barcode: str
    quantity: int  # Available quantity
    is_supply: bool = Field(alias="isSupply")
    is_realization: bool = Field(alias="isRealization")
    quantity_full: int = Field(alias="quantityFull")  # Total quantity
    warehouse_name: str = Field(alias="warehouseName")
    nm_id: int = Field(alias="nmId")
    subject: str
    category: str
    days_on_site: int = Field(alias="daysOnSite")
    brand: str
    sc_code: str = Field(alias="SCCode")
    price: float
    discount: float


class Order(WBBaseModel):
    """Order report item."""

    date: datetime
    last_change_date: datetime = Field(alias="lastChangeDate")
    supplier_article: str = Field(alias="supplierArticle")
    tech_size: str = Field(alias="techSize")
    barcode: str
    total_price: float = Field(alias="totalPrice")
    discount_percent: int = Field(alias="discountPercent")
    warehouse_name: str = Field(alias="warehouseName")
    oblast: str  # Region
    income_id: int = Field(alias="incomeID")
    odid: int  # Order ID
    nm_id: int = Field(alias="nmId")
    subject: str
    category: str
    brand: str
    is_cancel: bool = Field(alias="isCancel")
    cancel_dt: datetime | None = Field(alias="cancel_dt", default=None)


class Sale(WBBaseModel):
    """Sale report item."""

    date: datetime
    last_change_date: datetime = Field(alias="lastChangeDate")
    supplier_article: str = Field(alias="supplierArticle")
    tech_size: str = Field(alias="techSize")
    barcode: str
    total_price: float = Field(alias="totalPrice")
    discount_percent: int = Field(alias="discountPercent")
    is_supply: bool = Field(alias="isSupply")
    is_realization: bool = Field(alias="isRealization")
    promo_code_discount: float = Field(alias="promoCodeDiscount")
    warehouse_name: str = Field(alias="warehouseName")
    country_name: str = Field(alias="countryName")
    oblast_okrug_name: str = Field(alias="oblastOkrugName")
    region_name: str = Field(alias="regionName")
    income_id: int = Field(alias="incomeID")
    sale_id: str = Field(alias="saleID")
    odid: int
    spp: float  # Discount
    for_pay: float = Field(alias="forPay")  # To pay to seller
    finished_price: float = Field(alias="finishedPrice")
    price_with_disc: float = Field(alias="priceWithDisc")
    nm_id: int = Field(alias="nmId")
    subject: str
    category: str
    brand: str
    is_storno: int = Field(alias="IsStorno")  # Is return
    g_number: str = Field(alias="gNumber")
    sticker: str | None = None


# === Excise Report ===


class ExciseReportItem(WBBaseModel):
    """Excise (marking) report item."""

    retail_amount: float = Field(alias="retailAmount")
    date: date
    finishedPrice: float  # noqa: N815
    operation_type_name: str = Field(alias="operationTypeName")
    fiscal_dt: datetime = Field(alias="fiscalDt")
    doc_number: str = Field(alias="docNumber")
    fnumber: str
    reg_number: str = Field(alias="regNumber")
    contract_number: str = Field(alias="contractNumber")
    inn: str
    declaration_number: str = Field(alias="declarationNumber")
    gtin: str


# === Deduction Reports ===


class WarehouseMeasurement(WBBaseModel):
    """Warehouse measurement (size penalty) report item."""

    nm_id: int = Field(alias="nmId")
    sa_name: str = Field(alias="saName")  # Supplier article
    ts_name: str = Field(alias="tsName")  # Tech size
    barcode: str
    doc_type: str = Field(alias="docType")
    decision_date: date = Field(alias="decisionDate")
    penalty: float  # Penalty amount
    volume_real: float = Field(alias="volumeReal")
    volume_stated: float = Field(alias="volumeStated")
    length_real: float = Field(alias="lengthReal")
    length_stated: float = Field(alias="lengthStated")
    width_real: float = Field(alias="widthReal")
    width_stated: float = Field(alias="widthStated")
    height_real: float = Field(alias="heightReal")
    height_stated: float = Field(alias="heightStated")


class AntifraudDetail(WBBaseModel):
    """Antifraud (self-redemption) detail report item."""

    nm_id: int = Field(alias="nmId")
    sa_name: str = Field(alias="saName")
    ts_name: str = Field(alias="tsName")
    barcode: str
    doc_type: str = Field(alias="docType")
    quantity: int
    retail_price: float = Field(alias="retailPrice")
    deduction: float  # Deduction amount
    date_operation: date = Field(alias="dateOperation")
    sale_id: str = Field(alias="saleId")


class IncorrectAttachment(WBBaseModel):
    """Incorrect attachment (product substitution) report item."""

    nm_id: int = Field(alias="nmId")
    sa_name: str = Field(alias="saName")
    ts_name: str = Field(alias="tsName")
    barcode: str
    doc_type: str = Field(alias="docType")
    penalty: float
    date_operation: date = Field(alias="dateOperation")


class GoodsLabeling(WBBaseModel):
    """Goods labeling penalty report item."""

    nm_id: int = Field(alias="nmId")
    sa_name: str = Field(alias="saName")
    ts_name: str = Field(alias="tsName")
    barcode: str
    doc_type: str = Field(alias="docType")
    penalty: float
    date_operation: date = Field(alias="dateOperation")


class CharacteristicsChange(WBBaseModel):
    """Characteristics change penalty report item."""

    nm_id: int = Field(alias="nmId")
    sa_name: str = Field(alias="saName")
    ts_name: str = Field(alias="tsName")
    barcode: str
    doc_type: str = Field(alias="docType")
    penalty: float
    date_operation: date = Field(alias="dateOperation")
    characteristic_name: str = Field(alias="characteristicName")
    value_before: str = Field(alias="valueBefore")
    value_after: str = Field(alias="valueAfter")


# === Region Sales ===


class RegionSale(WBBaseModel):
    """Region sales report item."""

    date: date
    nm_id: int = Field(alias="nmId")
    barcode: str
    subject: str
    brand: str
    sa_name: str = Field(alias="saName")
    ts_name: str = Field(alias="tsName")
    warehouse_name: str = Field(alias="warehouseName")
    region: str
    quantity: int
    retail_price: float = Field(alias="retailPrice")
    retail_amount: float = Field(alias="retailAmount")
    sale_percent: int = Field(alias="salePercent")
    commission_percent: float = Field(alias="commissionPercent")
    supplier_oper_name: str = Field(alias="supplierOperName")
    order_date: date = Field(alias="orderDate")
    sale_date: date = Field(alias="saleDate")
    shk_id: int = Field(alias="shkId")
    retail_price_withdisc_rub: float = Field(alias="retailPriceWithdiscRub")
    delivery_amount: int = Field(alias="deliveryAmount")
    return_amount: int = Field(alias="returnAmount")
    delivery_rub: float = Field(alias="deliveryRub")
    gi_id: int = Field(alias="giId")
    subject_id: int = Field(alias="subjectId")
    nm_id_for: int = Field(alias="nmIdFor")
    brand_id: int = Field(alias="brandId")
    is_supplier_contract: bool = Field(alias="IsSupplierContract")
    sccode: str = Field(alias="sccode")


# === Brand Share ===


class Brand(WBBaseModel):
    """Brand information."""

    brand: str


class ParentSubject(WBBaseModel):
    """Parent subject (category) information."""

    parent_id: int = Field(alias="parentID")
    parent_name: str = Field(alias="parentName")


class BrandShare(WBBaseModel):
    """Brand share report item."""

    date: date
    brand: str
    subject: str
    shks_sum: int = Field(alias="shksSum")  # Total items sold
    delivery_rub_sum: float = Field(alias="deliveryRubSum")  # Total delivery revenue
    brand_share_percent: float = Field(alias="brandSharePercent")  # Brand share %


# === Report Tasks ===


class ReportTaskResponse(WBBaseModel):
    """Response when creating a report task."""

    task_id: str = Field(alias="taskId")
    status: str  # Task status
    created_at: datetime = Field(alias="createdAt")


class ReportTaskStatus(WBBaseModel):
    """Report task status."""

    task_id: str = Field(alias="taskId")
    status: str  # "processing", "completed", "failed"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    file_url: str | None = Field(alias="fileUrl", default=None)
    error: str | None = None

    @property
    def is_completed(self) -> bool:
        """Check if task is completed."""
        return self.status in ("completed", "done")

    @property
    def is_failed(self) -> bool:
        """Check if task failed."""
        return self.status == "failed"

    @property
    def is_processing(self) -> bool:
        """Check if task is still processing."""
        return self.status in ("processing", "pending", "in_progress")
