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

## Обработка ошибок

```python
from wb_api import (
    WBAPIError,
    WBAuthError,
    WBRateLimitError,
    WBValidationError
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
