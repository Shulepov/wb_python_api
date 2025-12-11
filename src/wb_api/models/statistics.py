"""Models for Statistics API (sales reports)."""

from datetime import datetime
from enum import Enum

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

class ReportPeriod(str, Enum):
    """Report period type."""

    DAILY = "daily"
    WEEKLY = "weekly"


class SalesReportItem(WBBaseModel):
    """Detailed sales report item (realization report)."""

    # Report identification
    realizationreport_id: int = Field(alias="realizationreport_id")
    srid: str = Field(alias="srid")
    date_from: datetime = Field(alias="date_from")
    date_to: datetime = Field(alias="date_to")
    create_dt: datetime = Field(alias="create_dt")
    suppliercontract_code: str | None = Field(alias="suppliercontract_code", default=None)

    # Pagination
    rrd_id: int = Field(alias="rrd_id")  # Row ID for pagination
    gi_id: int = Field(alias="gi_id")

    # Product information
    subject_name: str = Field(alias="subject_name")
    nm_id: int = Field(alias="nm_id")
    brand_name: str = Field(alias="brand_name")
    sa_name: str = Field(alias="sa_name")  # Subject area
    ts_name: str = Field(alias="ts_name")  # Tech size
    barcode: str = Field(alias="barcode")
    doc_type_name: str = Field(alias="doc_type_name")

    # Quantity and pricing
    quantity: int
    retail_price: float = Field(alias="retail_price")  # Retail price
    retail_amount: float = Field(alias="retail_amount")  # Total sales amount
    sale_percent: int = Field(alias="sale_percent")  # Seller discount %
    commission_percent: float = Field(alias="commission_percent")  # WB commission %

    # Office and operation
    office_name: str = Field(alias="office_name")
    supplier_oper_name: str = Field(alias="supplier_oper_name")
    order_dt: datetime = Field(alias="order_dt")
    sale_dt: datetime = Field(alias="sale_dt")
    rr_dt: datetime | None = Field(alias="rr_dt", default=None)
    shk_id: int = Field(alias="shk_id")
    retail_price_withdisc_rub: float = Field(alias="retail_price_withdisc_rub")

    # Logistics and delivery
    delivery_amount: int = Field(alias="delivery_amount", default=0)
    return_amount: int = Field(alias="return_amount", default=0)
    delivery_rub: float = Field(alias="delivery_rub", default=0.0)
    gi_box_type_name: str = Field(alias="gi_box_type_name")

    # Discounts and promotions
    product_discount_for_report: float = Field(alias="product_discount_for_report", default=0.0)
    supplier_promo: float = Field(alias="supplier_promo", default=0.0)
    #rid: int

    # WB calculations
    ppvz_spp_prc: float = Field(alias="ppvz_spp_prc", default=0.0)
    ppvz_kvw_prc_base: float = Field(alias="ppvz_kvw_prc_base", default=0.0)
    ppvz_kvw_prc: float = Field(alias="ppvz_kvw_prc", default=0.0)
    sup_rating_prc_up: float = Field(alias="sup_rating_prc_up", default=0.0)
    is_kgvp_v2: float = Field(alias="is_kgvp_v2", default=0.0)

    # Commission and fees
    ppvz_sales_commission: float = Field(alias="ppvz_sales_commission", default=0.0)
    ppvz_for_pay: float = Field(alias="ppvz_for_pay")  # AMOUNT TO PAY TO SELLER
    ppvz_reward: float = Field(alias="ppvz_reward", default=0.0)
    acquiring_fee: float = Field(alias="acquiring_fee", default=0.0)
    acquiring_percent: float = Field(alias="acquiring_percent", default=0.0)
    acquiring_bank: str = Field(alias="acquiring_bank", default="")

    # Additional WB fields
    ppvz_vw: float = Field(alias="ppvz_vw", default=0.0)
    ppvz_vw_nds: float = Field(alias="ppvz_vw_nds", default=0.0)
    ppvz_office_id: int = Field(alias="ppvz_office_id", default=0)
    ppvz_office_name: str = Field(alias="ppvz_office_name", default="")
    ppvz_supplier_id: int = Field(alias="ppvz_supplier_id", default=0)
    ppvz_supplier_name: str = Field(alias="ppvz_supplier_name", default="")
    ppvz_inn: str = Field(alias="ppvz_inn", default="")
    declaration_number: str = Field(alias="declaration_number", default="")
    bonus_type_name: str = Field(alias="bonus_type_name", default="")
    sticker_id: str = Field(alias="sticker_id", default="")
    site_country: str = Field(alias="site_country", default="")

    # Penalties and adjustments
    penalty: float = 0.0
    additional_payment: float = 0.0
    rebill_logistic_cost: float = Field(alias="rebill_logistic_cost", default=0.0)
    rebill_logistic_org: str = Field(alias="rebill_logistic_org", default="")
    kiz: str = ""
    storage_fee: float = Field(alias="storage_fee", default=0.0)
    deduction: float = 0.0
    acceptance: float = 0.0

    @property
    def total_to_seller(self) -> float:
        """Total amount to pay to seller."""
        return self.ppvz_for_pay

    @property
    def margin(self) -> float:
        """Seller margin (before commissions)."""
        return self.retail_amount - self.product_discount_for_report

    @property
    def total_fees(self) -> float:
        """Total fees (commission + acquiring + delivery)."""
        return (
            self.ppvz_sales_commission
            + self.acquiring_fee
            + abs(self.delivery_rub)
            + self.storage_fee
        )

    @property
    def net_profit(self) -> float:
        """Net profit (to seller - fees - penalties)."""
        return self.ppvz_for_pay - self.penalty + self.additional_payment


