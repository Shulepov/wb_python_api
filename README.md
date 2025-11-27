# Wildberries API Python SDK

Python библиотека для работы с API Wildberries.

## Возможности

- 🎯 Простой и понятный интерфейс
- 📦 Полное покрытие категорий API (Content, Analytics, Marketplace и др.)
- 🔒 Строгая типизация с Pydantic
- ⚡ Встроенный rate limiting (token bucket)
- 🔄 Поддержка синхронного и асинхронного кода
- 🧪 Поддержка sandbox окружения

## Установка

```bash
pip install wb-api
```

Или из исходников:

```bash
git clone https://github.com/yourusername/wb_python_api.git
cd wb_python_api
pip install -e .
```

## Быстрый старт

```python
from wb_api import WildberriesClient

# Создание клиента
client = WildberriesClient(token="your_api_token")

# Получение списка товаров
cards = client.content.get_cards(limit=10)
for card in cards.cards:
    print(f"{card.nm_id}: {card.title}")

# Использование контекстного менеджера
with WildberriesClient(token="your_token") as client:
    cards = client.content.get_cards()
```

## Использование

### Инициализация клиента

```python
from wb_api import WildberriesClient

# Базовая инициализация
client = WildberriesClient(token="your_api_token")

# С дополнительными параметрами
client = WildberriesClient(
    token="your_api_token",
    sandbox=True,  # Использовать sandbox окружение
    timeout=30.0,   # Таймаут запросов в секундах
    max_retries=3   # Максимальное количество повторов
)
```

### Работа с токеном

```python
from wb_api import TokenDecoder

# Декодирование токена
token_info = TokenDecoder.decode("your_token")
print(f"Seller ID: {token_info.seller_id}")
print(f"Token type: {token_info.token_type}")
print(f"Categories: {token_info.categories}")
print(f"Expires at: {token_info.expires_at}")
print(f"Read only: {token_info.is_read_only}")

# Проверка валидности токена
is_valid, error = TokenDecoder.validate_token("your_token")
if not is_valid:
    print(f"Token invalid: {error}")

# Проверка доступа к категории
has_access = TokenDecoder.has_category_access("your_token", "content")
```

### Content API - Работа с товарами

```python
# Получение категорий
categories = client.content.get_parent_categories()
for cat in categories:
    print(f"{cat.id}: {cat.name}")

# Получение предметов (подкатегорий)
subjects = client.content.get_subjects(parent_id=1234)

# Получение характеристик предмета
characteristics = client.content.get_subject_characteristics(subject_id=5678)

# Получение карточек товаров
response = client.content.get_cards(limit=100)
for card in response.cards:
    print(f"{card.nm_id}: {card.title} - {card.brand}")

# Поиск товаров
response = client.content.get_cards(text_search="iPhone", limit=50)

# Итератор по всем карточкам с автоматической пагинацией
for card in client.content.iter_cards(batch_size=100):
    print(card.vendor_code)

# Создание карточки товара
from wb_api.models.content import CreateCardRequest, CreateCardVariant, CreateCardSize

card = CreateCardRequest(
    subject_id=123,
    variants=[
        CreateCardVariant(
            vendor_code="ART-001",
            title="Название товара",
            description="Описание товара",
            brand="Бренд",
            dimensions={
                "length": 10,
                "width": 5,
                "height": 3,
                "weightBrutto": 0.5
            },
            sizes=[
                CreateCardSize(
                    tech_size="OneSize",
                    skus=["SKU-001"]
                )
            ]
        )
    ]
)
result = client.content.create_cards([card])

# Обновление карточек
client.content.update_cards([{
    "nmID": 123456,
    "vendorCode": "NEW-CODE"
}])

# Удаление карточек (перемещение в корзину)
client.content.delete_cards([123456, 123457])

# Восстановление карточек из корзины
client.content.recover_cards([123456])

# Загрузка медиафайлов по URL
client.content.upload_media_by_url(
    nm_id=123456,
    urls=["https://example.com/image1.jpg", "https://example.com/image2.jpg"]
)

# Работа с тегами
tag = client.content.create_tag(name="Новинка", color="FF0000")
client.content.delete_tag(tag_id=123)
```

### Common API - Общие методы

```python
# Проверка подключения
status = client.ping()
print(status)

# Получение тарифов
tariffs = client.common.get_tariffs()
commission = client.common.get_tariffs_commission()
```

### Prices API - Работа с ценами и скидками

```python
from wb_api.models.prices import Price, SizePrice, ClubDiscount

# Загрузка цен и скидок
prices = [
    Price(nm_id=123456, price=1500, discount=20),  # 20% скидка
    Price(nm_id=123457, price=2000, discount=15),  # 15% скидка
]
response = client.prices.upload_prices(prices)
print(f"Task ID: {response.task_id}")

# Ожидание завершения загрузки
result = client.prices.wait_for_task(response.task_id, timeout=60)
print(f"Processed: {result.processed_items}/{result.total_items}")

# Ожидание с отслеживанием прогресса
def show_progress(task):
    print(f"Progress: {task.progress_percent:.1f}%")

result = client.prices.wait_for_task(
    response.task_id,
    on_progress=show_progress,
    interval=3
)

# Загрузка цен для конкретных размеров
size_prices = [
    SizePrice(size_id=789012, price=1200),
]
client.prices.upload_size_prices(size_prices)

# Загрузка скидок WB Клуба (0-50%)
club_discounts = [
    ClubDiscount(nm_id=123456, club_discount=10),
]
client.prices.upload_club_discounts(club_discounts)

# Получение товаров с ценами
goods = client.prices.get_goods_with_prices(limit=100)
for good in goods:
    print(f"{good.vendor_code}: {good.price}₽ (-{good.discount}%)")

# Получение по артикулам
goods = client.prices.get_goods_by_vendor_codes(["ART-001", "ART-002"])

# Получение цен для всех размеров товара
sizes = client.prices.get_size_prices(nm_id=123456)
for size in sizes:
    print(f"Size {size.tech_size}: {size.price}₽")

# Итератор по всем товарам с ценами
for good in client.prices.iter_goods_with_prices(batch_size=500):
    print(f"{good.nm_id}: {good.price}₽")

# Проверка товаров в карантине
quarantine = client.prices.get_quarantine_goods()
for good in quarantine:
    print(f"{good.vendor_code}: {good.reason}")

# Мониторинг задач
processed_tasks = client.prices.get_processed_tasks(limit=10)
pending_tasks = client.prices.get_pending_tasks()
```

### Finance API - Баланс продавца

```python
# Получить баланс
balance = client.finance.get_balance()
print(f"Валюта: {balance.currency}")
print(f"На счёте: {balance.current}₽")
print(f"Доступно к выводу: {balance.for_withdraw}₽")
print(f"Заблокировано: {balance.blocked}₽ ({balance.blocked_percent:.1f}%)")
```

**⚠️ Важно**: Rate Limit - **1 запрос в минуту**!

### Statistics API - Отчёты о продажах

```python
from datetime import datetime, timedelta

# Отчёт за последние 30 дней
date_to = datetime.now()
date_from = date_to - timedelta(days=30)

# Получить детальный отчёт
report = client.statistics.get_sales_report(
    date_from=date_from,
    date_to=date_to,
    period="daily"
)

# Анализ отчёта
for item in report:
    print(f"NM ID: {item.nm_id}")
    print(f"Товар: {item.subject_name}")
    print(f"Количество: {item.quantity}")
    print(f"Выручка: {item.retail_amount}₽")
    print(f"К оплате продавцу: {item.total_to_seller}₽")
    print(f"Комиссия WB: {item.ppvz_sales_commission}₽")
    print(f"Маржа: {item.margin}₽")
    print(f"Чистая прибыль: {item.net_profit}₽")
    print()

# Итератор по всему отчёту (автоматическая пагинация)
total_to_seller = 0
for item in client.statistics.iter_sales_report(date_from, date_to):
    total_to_seller += item.total_to_seller

print(f"Итого к оплате за период: {total_to_seller}₽")

# Получить сводку
summary = client.statistics.get_sales_summary(
    date_from=date_from,
    date_to=date_to
)
print(f"\n=== Сводка за период ===")
print(f"Всего позиций: {summary.total_items}")
print(f"Продано единиц: {summary.quantity_sold}")
print(f"Выручка: {summary.revenue}₽")
print(f"К оплате продавцу: {summary.to_seller}₽")
print(f"Комиссия WB: {summary.commission}₽ ({summary.commission_percent:.1f}%)")
print(f"Логистика: {summary.delivery_cost}₽")
print(f"Эквайринг: {summary.acquiring_fee}₽")
print(f"Штрафы: {summary.penalty}₽")
print(f"Хранение: {summary.storage_fee}₽")
print(f"Чистыми: {summary.net_to_seller}₽")
print(f"Средний чек: {summary.average_order_value:.2f}₽")
```

**⚠️ Важно**:
- Rate Limit - **1 запрос в минуту**!
- Данные доступны с 29 января 2024
- До 100,000 строк за запрос
- 50+ полей в каждой строке отчёта

### Marketing API - Рекламные кампании (только чтение)

```python
from datetime import datetime, timedelta

# === Список кампаний ===
campaigns = client.marketing.list_campaigns()
print(f"Всего кампаний: {len(campaigns.all)}")
print(f"Активных: {len(campaigns.active)}")
print(f"На паузе: {len(campaigns.paused)}")

# === Информация о кампаниях ===
campaign_ids = campaigns.active[:5]  # Первые 5 активных
campaigns_info = client.marketing.get_campaigns_info(campaign_ids)
for camp in campaigns_info:
    print(f"ID: {camp.campaign_id}, Название: {camp.name}, Тип: {camp.type}")

# === Статистика кампаний ===
date_to = datetime.now()
date_from = date_to - timedelta(days=7)

stats = client.marketing.get_full_stats(
    campaign_ids=[12345, 12346],
    date_from=date_from,
    date_to=date_to
)

for stat in stats:
    print(f"\n=== Кампания {stat.campaign_id} ({stat.name}) ===")
    print(f"Показы: {stat.views:,}")
    print(f"Клики: {stat.clicks} (CTR: {stat.ctr:.2f}%)")
    print(f"Расход: {stat.sum_:,.2f}₽ (CPC: {stat.cpc:.2f}₽)")
    print(f"Заказы: {stat.orders} (CR: {stat.cr:.2f}%)")
    print(f"Сумма заказов: {stat.sum_price:,.2f}₽")
    print(f"ROAS: {stat.roas:.2f}")
    print(f"CPO: {stat.cost_per_order:.2f}₽")
    print(f"Средний чек: {stat.avg_order_value:.2f}₽")

# === Статистика по ключевым словам ===
keywords = client.marketing.get_keyword_stats(campaign_id=12345)
for kw in keywords[:10]:
    print(f"Запрос: {kw.keyword}")
    print(f"  Показы: {kw.views}, Клики: {kw.clicks}, Заказы: {kw.orders}")
    print(f"  Расход: {kw.sum_:.2f}₽, ROAS: {kw.sum_price/kw.sum_ if kw.sum_ else 0:.2f}")

# === Статистика по кластерам ===
clusters = client.marketing.get_cluster_stats(
    campaign_id=12345,
    date_from=date_from,
    date_to=date_to
)
for cluster in clusters[:10]:
    print(f"Кластер: {cluster.cluster} (запросов: {cluster.count})")
    print(f"  Показы: {cluster.views}, Клики: {cluster.clicks}, Заказы: {cluster.orders}")

# === Финансы рекламного счёта ===
balance = client.marketing.get_balance()
print(f"\n=== Баланс рекламного счёта ===")
print(f"Доступно: {balance.balance:,.2f}₽")
print(f"Бонусы: {balance.bonus:,.2f}₽")
print(f"Всего: {balance.total:,.2f}₽")

# === История затрат ===
expenses = client.marketing.get_expenses_history(
    date_from=date_from,
    date_to=date_to
)
total_spent = sum(exp.sum_ for exp in expenses)
print(f"\nИтого затрат за период: {total_spent:,.2f}₽")
for exp in expenses[:5]:
    print(f"{exp.date}: {exp.campaign_name} - {exp.sum_:.2f}₽")

# === История пополнений ===
payments = client.marketing.get_payments_history(
    date_from=date_from,
    date_to=date_to
)
total_deposited = sum(pay.sum_ for pay in payments)
print(f"\nИтого пополнений за период: {total_deposited:,.2f}₽")
```

**Rate Limit**: 60 запросов/минуту

### Promotions API - Акции на календаре (только чтение)

```python
# === Список акций ===
promotions = client.promotions.get_promotions_list()
print(f"Найдено акций: {len(promotions)}")

for promo in promotions:
    print(f"\nАкция: {promo.name}")
    print(f"ID: {promo.promotion_id}")
    print(f"Период: {promo.start_date} - {promo.end_date}")
    print(f"Активна: {promo.is_active}")

# === Детали акции ===
if promotions:
    promo_id = promotions[0].promotion_id
    details = client.promotions.get_promotions_details(promo_id)

    print(f"\n=== Детали акции {details.name} ===")
    print(f"Описание: {details.description}")
    print(f"Тип: {details.type}")
    print(f"Механика: {details.mechanic}")
    if details.discount_value:
        print(f"Скидка: {details.discount_value}% ({details.discount_type})")
    if details.min_price:
        print(f"Минимальная цена: {details.min_price}₽")
    if details.max_price:
        print(f"Максимальная цена: {details.max_price}₽")
    print(f"Категории: {', '.join(details.categories)}")

# === Товары для акции ===
if promotions:
    items = client.promotions.get_promotion_items(promotions[0].promotion_id)

    print(f"\n=== Товары доступные для участия ({len(items)}) ===")
    for item in items[:10]:
        print(f"\nNM ID: {item.nm_id}")
        print(f"Артикул: {item.vendor_code}")
        print(f"Название: {item.title}")
        print(f"Цена: {item.price}₽ (скидка {item.discount}%)")
        if item.promo_price:
            print(f"Цена с акцией: {item.promo_price}₽")
        print(f"Участвует: {'Да' if item.is_participating else 'Нет'}")
        print(f"Доступен: {'Да' if item.is_available else 'Нет'}")
        print(f"Остаток: {item.stock} шт.")
```

**Rate Limit**: 60 запросов/минуту

### Reports API - Отчёты и аналитика

```python
from datetime import datetime, timedelta

date_to = datetime.now()
date_from = date_to - timedelta(days=7)

# === Основные отчёты (Rate Limit: 1 req/min) ===

# Поставки
incomes = client.reports.get_incomes(date_from=date_from)
print(f"Поставок: {len(incomes)}")
for income in incomes[:5]:
    print(f"Поставка №{income.number}: {income.quantity} шт, {income.total_price}₽")

# Остатки на складах
stocks = client.reports.get_stocks(date_from=date_from)
total_quantity = sum(s.quantity for s in stocks)
print(f"\nВсего остатков: {total_quantity} шт на {len(stocks)} позиций")

# Заказы
orders = client.reports.get_orders(date_from=date_from, flag=0)
total_orders = sum(1 for o in orders if not o.is_cancel)
print(f"\nЗаказов: {total_orders} (отменено: {len(orders) - total_orders})")

# Продажи и возвраты
sales = client.reports.get_sales(date_from=date_from, flag=0)
revenue = sum(s.for_pay for s in sales if s.is_storno == 0)
returns = sum(1 for s in sales if s.is_storno == 1)
print(f"\nПродано: {len(sales) - returns}, возвратов: {returns}")
print(f"Выручка: {revenue:,.2f}₽")

# === Региональная аналитика ===

region_sales = client.reports.get_region_sales(date_from=date_from, date_to=date_to)
by_region = {}
for sale in region_sales:
    region = sale.region
    if region not in by_region:
        by_region[region] = {"quantity": 0, "revenue": 0}
    by_region[region]["quantity"] += sale.quantity
    by_region[region]["revenue"] += sale.retail_amount

print("\n=== Продажи по регионам ===")
for region, data in sorted(by_region.items(), key=lambda x: x[1]["revenue"], reverse=True)[:10]:
    print(f"{region}: {data['quantity']} шт, {data['revenue']:,.2f}₽")

# === Штрафы и удержания ===

# Штрафы за габариты
measurements = client.reports.get_warehouse_measurements(date_from, date_to)
total_penalty = sum(m.penalty for m in measurements)
print(f"\nШтрафы за габариты: {total_penalty:,.2f}₽ ({len(measurements)} позиций)")

# Штрафы за самовыкупы
antifraud = client.reports.get_antifraud_details(date_from, date_to)
antifraud_penalty = sum(a.deduction for a in antifraud)
print(f"Штрафы за самовыкупы: {antifraud_penalty:,.2f}₽ ({len(antifraud)} товаров)")

# Штрафы за подмены
attachments = client.reports.get_incorrect_attachments(date_from, date_to)
attachments_penalty = sum(a.penalty for a in attachments)
print(f"Штрафы за подмены: {attachments_penalty:,.2f}₽ ({len(attachments)} случаев)")

# Штрафы за маркировку
labeling = client.reports.get_goods_labeling(date_from, date_to)
labeling_penalty = sum(l.penalty for l in labeling)
print(f"Штрафы за маркировку: {labeling_penalty:,.2f}₽")

# Штрафы за смену характеристик
characteristics = client.reports.get_characteristics_change(date_from, date_to)
char_penalty = sum(c.penalty for c in characteristics)
print(f"Штрафы за смену характеристик: {char_penalty:,.2f}₽")

print(f"\nВсего штрафов: {sum([total_penalty, antifraud_penalty, attachments_penalty, labeling_penalty, char_penalty]):,.2f}₽")

# === Доля бренда ===

brands = client.reports.get_brand_list()
print(f"\n=== Ваши бренды ({len(brands)}) ===")
for brand in brands:
    print(f"- {brand.brand}")

    # Категории бренда
    subjects = client.reports.get_parent_subjects(brand.brand)
    for subject in subjects[:3]:
        # Доля бренда в категории
        share = client.reports.get_brand_share(
            brand=brand.brand,
            subject_id=subject.parent_id,
            date_from=date_from,
            date_to=date_to
        )
        if share:
            print(f"  {subject.parent_name}: доля {share[0].brand_share_percent:.1f}%")

# === Генерируемые отчёты (с системой задач) ===

# Отчёт об остатках на складах (детальный)
print("\n=== Генерация отчёта об остатках ===")
task = client.reports.create_warehouse_remains()
print(f"Задача создана: {task.task_id}")

# Ждём готовности
status = client.reports.wait_for_warehouse_remains(task.task_id, timeout=300)
if status.is_completed:
    print("Отчёт готов!")
    # Скачиваем файл
    report_data = client.reports.download_warehouse_remains(task.task_id)
    with open("warehouse_remains.xlsx", "wb") as f:
        f.write(report_data)
    print(f"Отчёт сохранён: warehouse_remains.xlsx ({len(report_data)} байт)")

# Аналогично для других отчётов:
# - create_acceptance_report() -> wait_for_acceptance_report() -> download_acceptance_report()
# - create_paid_storage() -> wait_for_paid_storage() -> download_paid_storage()
```

**⚠️ Важно**:
- Основные отчёты: Rate Limit **1 запрос/минуту**
- Некоторые методы имеют особые лимиты (см. документацию)
- Генерируемые отчёты возвращают Excel/CSV файлы
- Используйте wait_for_* методы для ожидания готовности отчётов

## Обработка ошибок

```python
from wb_api import (
    WBAPIError,
    WBAuthError,
    WBRateLimitError,
    WBValidationError,
    WBTaskTimeoutError,
    WBTaskFailedError,
)

try:
    cards = client.content.get_cards()
except WBAuthError as e:
    print(f"Authentication failed: {e}")
except WBRateLimitError as e:
    print(f"Rate limit exceeded, retry after {e.retry_after}s")
except WBValidationError as e:
    print(f"Validation error: {e}")
except WBAPIError as e:
    print(f"API error: {e.status_code} - {e.message}")

# Обработка ошибок при работе с задачами
try:
    response = client.prices.upload_prices(prices)
    result = client.prices.wait_for_task(response.task_id, timeout=60)
except WBTaskTimeoutError as e:
    print(f"Task {e.task_id} timeout after {e.timeout}s")
except WBTaskFailedError as e:
    print(f"Task {e.task_id} failed: {e.task_status}")
    print(f"Errors: {e.task_errors}")
```

## Rate Limiting

Библиотека автоматически управляет ограничениями скорости (rate limiting) для каждой категории API:

- Content API: 100 запросов/минуту (burst: 5)
- Marketplace API: 300 запросов/минуту (burst: 20)
- И т.д.

Rate limiter использует алгоритм token bucket и автоматически обновляется на основе заголовков ответа API.

## Структура проекта

```
wb-api/
├── src/
│   └── wb_api/
│       ├── __init__.py          # Публичный API
│       ├── client.py            # Главный клиент
│       ├── config.py            # Конфигурация
│       ├── auth.py              # Работа с токенами
│       ├── exceptions.py        # Исключения
│       ├── rate_limiter.py      # Rate limiting
│       ├── constants.py         # Константы
│       ├── models/              # Pydantic модели
│       │   ├── base.py
│       │   ├── content.py
│       │   └── ...
│       ├── api/                 # API модули
│       │   ├── base.py
│       │   ├── content.py
│       │   ├── common.py
│       │   └── ...
│       └── utils/               # Утилиты
└── tests/                       # Тесты
```

## Требования

- Python >= 3.10
- httpx >= 0.27.0
- pydantic >= 2.0
- pyjwt >= 2.8.0

## Разработка

```bash
# Установка зависимостей для разработки
pip install -e ".[dev]"

# Запуск тестов
pytest

# Линтинг
ruff check .

# Проверка типов
mypy src/wb_api
```

## Лицензия

MIT

## Ссылки

- [Документация Wildberries API](https://dev.wildberries.ru/openapi/api-information)
- [Content API](https://dev.wildberries.ru/openapi/work-with-products)
- [Analytics API](https://dev.wildberries.ru/openapi/analytics)
- [Marketplace API](https://dev.wildberries.ru/openapi/marketplace)
