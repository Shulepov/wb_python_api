"""Models for Reports API."""

from datetime import date, datetime

from pydantic import Field

from .base import WBBaseModel

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
