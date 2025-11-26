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
