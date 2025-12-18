"""Models for Marketing API (Promotion/Advertising)."""

from datetime import date, datetime
from enum import Enum

from pydantic import Field

from .base import WBBaseModel


class CampaignType(int, Enum):
    """Campaign type."""

    SEARCH_AUTO = 4  # Поиск - автоматическая
    SEARCH_PLACEMENT = 5  # Поиск + Каталог
    SEARCH_MANUAL = 6  # Поиск - ручная ставка
    CATALOG = 7  # Каталог
    UNIFIED_BID = 8  # Единая ставка
    AUCTION = 9  # Аукцион


class CampaignStatus(int, Enum):
    """Campaign status."""

    DELETED = -1  # Удалена
    PREPARING = 4  # Готовится к запуску
    COMPLETED = 7  # Завершена
    CANCELED = 8  # Отменена
    ACTIVE = 9  # Активна
    PAUSED = 11  # На паузе


class PaymentStatus(int, Enum):
    """Campaign status."""

    ERROR = 0  # Ошибка
    HANDLED = 1  # Обработано


class PaymentType(str, Enum):
    CPM = "cpm"
    CPS = "cpc"


class AdvertShortInfo(WBBaseModel):
    id: int = Field(alias="advertId")
    change_time: datetime = Field(alias="changeTime")


class CampaignsGroupByTypeAndStatus(WBBaseModel):
    """Campaign basic information."""

    type: CampaignType = Field(alias="type")
    status: CampaignStatus = Field(alias="status")
    count: int = Field(alias="count")
    advert_list: list[AdvertShortInfo] = Field(
        alias="advert_list", default_factory=list
    )


class CampaignListResponse(WBBaseModel):
    """Response with list of campaigns."""

    all: int = Field(alias="all")  # All campaigns amount
    adverts: list[CampaignsGroupByTypeAndStatus] = Field(
        alias="adverts", default_factory=list
    )


class AdvertBidsKopecks(WBBaseModel):
    search: int = Field(alias="search")
    recommendations: int = Field(alias="recommendations")


class AdvertSubject(WBBaseModel):
    id: int = Field(alias="id")
    name: str = Field(alias="name")


class AdvertNMsSettings(WBBaseModel):
    bids_kopecks: AdvertBidsKopecks = Field(alias="bids_kopecks")
    subject: AdvertSubject = Field(alias="subject")
    nm_id: int = Field(alias="nm_id")


class AdvertPlacement(WBBaseModel):
    search: bool = Field(alias="search")
    recommendations: bool = Field(alias="recommendations")


class AdvertSettings(WBBaseModel):
    payment_type: PaymentType = Field(alias="payment_type")
    name: str = Field(alias="name")
    placements: AdvertPlacement = Field(alias="placements")


class AdvertTimestamps(WBBaseModel):
    created: datetime = Field(alias="created")
    updated: datetime = Field(alias="updated")
    started: datetime = Field(alias="started")
    deleted: datetime = Field(alias="deleted")


class CampaignInfo(WBBaseModel):
    """Detailed campaign information."""

    campaign_id: int = Field(alias="id")
    bid_type: str = Field(alias="bid_type")
    nm_settings: list[AdvertNMsSettings] = Field(
        alias="nm_settings", default_factory=list
    )
    settings: AdvertSettings = Field(alias="settings")
    status: CampaignStatus = Field(alias="status")
    timestamps: AdvertTimestamps = Field(alias="timestamps")


class BoosterStats(WBBaseModel):
    avg_position: int = Field(alias="avg_position")
    date_of_data: date = Field(alias="date")
    nm_id: int = Field(alias="nm")


class AdvertBaseStats(WBBaseModel):
    atbs: int = 0  # Добавления в корзину
    views: int = Field(alias="views")
    cancels: int = Field(alias="canceled")
    clicks: int = Field(alias="clicks")
    cpc: float = Field(alias="cpc")
    cr: float = Field(alias="cr")
    ctr: float = Field(alias="ctr")
    orders: int = Field(alias="orders")
    shks: int = Field(alias="shks")
    total_spend: float = Field(alias="sum")  # total spend
    orders_value: float = Field(alias="sum_price")


class CampaignDailyStats(AdvertBaseStats):
    apps: dict = Field(alias="apps", default_factory=dict)
    date_of_data: date = Field(alias="date")


class CampaignStats(AdvertBaseStats):
    """Campaign statistics."""

    campaign_id: int = Field(alias="advertId")

    booster_stats: list[BoosterStats] = Field(
        alias="booster_stats", default_factory=list
    )

    @property
    def avg_order_value(self) -> float:
        """Average order value."""
        return self.orders_value / self.orders if self.orders > 0 else 0.0

    @property
    def roas(self) -> float:
        """Return on ad spend."""
        return self.orders_value / self.total_spend if self.total_spend > 0 else 0.0

    @property
    def cost_per_order(self) -> float:
        """Cost per order (CPO)."""
        return self.total_spend / self.orders if self.orders > 0 else 0.0


class KeywordClusterStats(WBBaseModel):
    cluster: str = Field(alias="cluster")
    count: int = Field(alias="count")
    keywords: list[str] = Field(alias="keywords", default_factory=list)


class KeywordStats(WBBaseModel):
    """Keyword statistics."""

    excluded: list[str] = Field(alias="excluded", default_factory=list)
    clusters: list[KeywordClusterStats] = Field(alias="clusters", default_factory=list)


class ClusterStatsDetails(WBBaseModel):
    cluster: str = Field(alias="norm_query")  # Normalized query cluster
    views: int = Field(alias="views")
    clicks: int = Field(alias="clicks")
    atbs: int = Field(alias="atbs")
    orders: int = Field(alias="orders")
    ctr: float = Field(alias="ctr")
    cpc: float = Field(alias="cpc")
    cpm: float = Field(alias="cpm")
    avg_pos: float = Field(alias="avg_pos")


class ClusterStats(WBBaseModel):
    """Search cluster statistics."""

    campaign_id: int = Field(alias="advert_id")
    nm_id: int = Field(alias="nm_id")
    stats: list[ClusterStatsDetails] = Field(alias="stats", default_factory=list)


class PromoBonus(WBBaseModel):
    sum: int = Field(alias="sum")
    percent: int = Field(alias="percent")
    expiration_date: str = Field(alias="expiration_date")


class Balance(WBBaseModel):
    """Advertising account balance."""

    balance: float  # Current balance (rubles)
    net: float  # Available for withdrawal (rubles)
    bonus: float = 0.0  # Bonus balance (rubles)
    cashbacks: list[PromoBonus] = Field(alias="cashbacks", default_factory=list)

    @property
    def total(self) -> float:
        """Total balance including bonus."""
        return self.balance + self.bonus


class CampaignBudget(WBBaseModel):
    """Campaign budget information."""

    unused_cash: int = Field(alias="cash")
    unused_netting: int = Field(alias="netting")  # unused - always 0
    total: int = Field(alias="total")


class Expense(WBBaseModel):
    """Advertising expense record."""

    campaign_id: int = Field(alias="advertId")
    campaign_name: str = Field(alias="campName")
    upd_num: int = Field(alias="updNum")  # Номер выставленного документа
    upd_time: datetime | None = Field(alias="updTime", default=None)
    advert_type: int = Field(alias="advertType")  # Тип кампании
    payment_type: str = Field(alias="paymentType")  # Источник списания
    advert_status: CampaignStatus = Field(alias="advertStatus")
    upd_sum: float = Field(alias="updSum")  # Expense amount (rubles)


class Payment(WBBaseModel):
    """Advertising payment record."""

    id: int = Field(alias="id")  # id платежа
    date: datetime = Field(alias="date")  # дата платежа
    sum: float = Field(alias="sum")  # Payment amount (rubles)
    type: str  # Тип источника списания
    status: PaymentStatus = Field(alias="statusId")  # Payment status
    card_status: str = Field(alias="cardStatus")  # Статус операции(при оплате картой
