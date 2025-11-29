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
    DELETED = -1 # Удалена
    PREPARING = 4  # Готовится к запуску
    PAUSED = 7  # На паузе
    CANCELED = 8 # Отменена
    ACTIVE = 9  # Активна
    COMPLETED = 11  # Завершена

class PaymentStatus(int, Enum):
    """Campaign status."""
    ERROR = 0 # Ошибка
    HANDLED = 1  # Обработано

class Campaign(WBBaseModel):
    """Campaign basic information."""

    campaign_id: int = Field(alias="advertId")
    name: str
    type: CampaignType
    status: CampaignStatus
    created_at: datetime = Field(alias="createTime")
    updated_at: datetime = Field(alias="changeTime")
    start_date: datetime | None = Field(alias="startTime", default=None)
    end_date: datetime | None = Field(alias="endTime", default=None)



class CampaignListResponse(WBBaseModel):
    """Response with list of campaigns."""

    all: int = Field(alias="all")  # All campaigns amount
    adverts: list[dict] = Field(alias="adverts", default_factory=list)


class CampaignInfo(WBBaseModel):
    """Detailed campaign information."""

    campaign_id: int = Field(alias="advertId")
    type: int
    status: int
    name: str
    params: list[dict] = Field(default_factory=list)  # Campaign parameters
    create_time: datetime = Field(alias="createTime")
    change_time: datetime = Field(alias="changeTime")
    start_time: datetime | None = Field(alias="startTime", default=None)
    end_time: datetime | None = Field(alias="endTime", default=None)
    daily_budget: int | None = Field(alias="dailyBudget", default=None)

    # Additional fields for auction campaigns
    search_plus_state: bool | None = Field(alias="searchPluseState", default=None)
    united_params: list[dict] | None = Field(alias="unitedParams", default=None)


class CampaignStats(WBBaseModel):
    """Campaign statistics."""

    campaign_id: int = Field(alias="advertId")
    name: str | None = None
    views: int = 0  # Показы
    clicks: int = 0  # Клики
    ctr: float = 0.0  # CTR (%)
    cpc: float = 0.0  # CPC (средняя стоимость клика)
    sum_: float = Field(alias="sum", default=0.0)  # Расход (руб)
    atbs: int = 0  # Добавления в корзину
    orders: int = 0  # Заказы
    cr: float = 0.0  # CR (конверсия заказов, %)
    shks: int = 0  # Заказано товаров (шт)
    sum_price: float = Field(alias="sum_price", default=0.0)  # Заказано на сумму (руб)

    # Date range
    date_from: date | None = None
    date_to: date | None = None

    @property
    def avg_order_value(self) -> float:
        """Average order value."""
        return self.sum_price / self.orders if self.orders > 0 else 0.0

    @property
    def roas(self) -> float:
        """Return on ad spend."""
        return self.sum_price / self.sum_ if self.sum_ > 0 else 0.0

    @property
    def cost_per_order(self) -> float:
        """Cost per order (CPO)."""
        return self.sum_ / self.orders if self.orders > 0 else 0.0


class DailyStats(WBBaseModel):
    """Daily campaign statistics."""

    campaign_id: int = Field(alias="advertId")
    date: date
    views: int = 0
    clicks: int = 0
    ctr: float = 0.0
    cpc: float = 0.0
    sum_: float = Field(alias="sum", default=0.0)
    atbs: int = 0
    orders: int = 0
    cr: float = 0.0
    shks: int = 0
    sum_price: float = Field(alias="sum_price", default=0.0)


class KeywordStats(WBBaseModel):
    """Keyword statistics."""

    keyword: str
    views: int = 0
    clicks: int = 0
    ctr: float = 0.0
    cpc: float = 0.0
    sum_: float = Field(alias="sum", default=0.0)
    atbs: int = 0
    orders: int = 0
    cr: float = 0.0
    shks: int = 0
    sum_price: float = Field(alias="sum_price", default=0.0)


class ClusterStats(WBBaseModel):
    """Search cluster statistics."""

    cluster: str  # Normalized query cluster
    count: int = 0  # Number of queries in cluster
    views: int = 0
    clicks: int = 0
    ctr: float = 0.0
    cpc: float = 0.0
    sum_: float = Field(alias="sum", default=0.0)
    atbs: int = 0
    orders: int = 0
    cr: float = 0.0
    shks: int = 0
    sum_price: float = Field(alias="sum_price", default=0.0)


class Balance(WBBaseModel):
    """Advertising account balance."""

    balance: float  # Current balance (rubles)
    net: float  # Available for withdrawal (rubles)
    bonus: float = 0.0  # Bonus balance (rubles)

    @property
    def total(self) -> float:
        """Total balance including bonus."""
        return self.balance + self.bonus


class CampaignBudget(WBBaseModel):
    """Campaign budget information."""

    campaign_id: int = Field(alias="advertId")
    budget: float  # Current budget (rubles)
    daily_budget: float | None = Field(alias="dailyBudget", default=None)


class Expense(WBBaseModel):
    """Advertising expense record."""

    campaign_id: int = Field(alias="advertId")
    campaign_name: str = Field(alias="campName")
    upd_num: int = Field(alias="updNum") # Номер выставленного документа
    upd_time: str | None = Field(alias="updTime", default=None)
    advert_type: int = Field(alias="advertType") #Тип кампании
    payment_type: str = Field(alias="paymentType") #Источник списания
    advert_status: CampaignStatus = Field(alias="advertStatus")
    upd_sum: float = Field(alias="updSum")  # Expense amount (rubles)


class Payment(WBBaseModel):
    """Advertising payment record."""
    id: int = Field(alias="id") #id платежа
    date: datetime = Field(alias="date") #дата платежа
    sum: float = Field(alias="sum")  # Payment amount (rubles)
    type: str  # Тип источника списания
    status: PaymentStatus = Field(alias="statusId")  # Payment status
    card_status: str = Field(alias="cardStatus") #Статус операции(при оплате картой
