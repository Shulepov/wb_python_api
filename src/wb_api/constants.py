"""Constants for Wildberries API."""

# API domains by category
DOMAINS = {
    "content": "content-api.wildberries.ru",
    "analytics": "seller-analytics-api.wildberries.ru",
    "prices": "discounts-prices-api.wildberries.ru",
    "marketplace": "marketplace-api.wildberries.ru",
    "statistics": "statistics-api.wildberries.ru",
    "promotion": "advert-api.wildberries.ru",
    "feedbacks": "feedbacks-api.wildberries.ru",
    "chat": "buyer-chat-api.wildberries.ru",
    "supplies": "supplies-api.wildberries.ru",
    "returns": "returns-api.wildberries.ru",
    "documents": "documents-api.wildberries.ru",
    "finance": "finance-api.wildberries.ru",
    "common": "common-api.wildberries.ru",
}

# Sandbox domains (not all categories support sandbox)
SANDBOX_DOMAINS = {
    "content": "content-api-sandbox.wildberries.ru",
    "prices": "discounts-prices-api-sandbox.wildberries.ru",
    "statistics": "statistics-api-sandbox.wildberries.ru",
    "promotion": "advert-api-sandbox.wildberries.ru",
    "feedbacks": "feedbacks-api-sandbox.wildberries.ru",
}

# Default rate limits (requests per minute and burst capacity)
DEFAULT_RATE_LIMITS = {
    "content": {"rpm": 100, "burst": 5},
    "analytics": {"rpm": 60, "burst": 10},
    "prices": {"rpm": 100, "burst": 5},  # 10 req / 6 sec
    "marketplace": {"rpm": 300, "burst": 20},
    "statistics": {"rpm": 60, "burst": 10},
    "promotion": {"rpm": 60, "burst": 10},
    "feedbacks": {"rpm": 100, "burst": 10},
    "chat": {"rpm": 60, "burst": 10},
    "supplies": {"rpm": 60, "burst": 10},
    "returns": {"rpm": 60, "burst": 10},
    "documents": {"rpm": 60, "burst": 10},
    "finance": {"rpm": 60, "burst": 10},
    "common": {"rpm": 60, "burst": 10},
}

# HTTP headers
HEADER_RATELIMIT_REMAINING = "x-ratelimit-remaining"
HEADER_RATELIMIT_RETRY = "x-ratelimit-retry"
HEADER_RATELIMIT_RESET = "x-ratelimit-reset"
HEADER_RATELIMIT_LIMIT = "x-ratelimit-limit"
