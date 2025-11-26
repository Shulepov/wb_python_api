"""Example usage of Wildberries API SDK."""

from wb_api import WildberriesClient

# Replace with your actual API token
TOKEN = ""


def main():
    """Main example function."""
    # Initialize client
    with WildberriesClient(token=TOKEN, sandbox=False) as client:
        # Get token information
        token_info = client.token_info
        print(f"Seller ID: {token_info.seller_id}")
        print(f"Token type: {token_info.token_type}")
        print(f"Categories: {', '.join(token_info.categories)}")
        print(f"Expires at: {token_info.expires_at}")
        print()

        # Check API connection
        print("Checking API connection...")
        try:
            status = client.ping()
            print(f"Ping successful: {status}")
        except Exception as e:
            print(f"Ping failed: {e}")
        print()

        # Get parent categories
        print("Getting parent categories...")
        try:
            categories = client.content.get_parent_categories()
            print(f"Found {len(categories)} categories:")
            for cat in categories[:5]:
                print(f"  - {cat.name} (ID: {cat.id})")
        except Exception as e:
            print(f"Failed to get categories: {e}")
        print()

        # Get product cards
        print("Getting product cards...")
        try:
            response = client.content.get_cards(limit=100)
            print(f"Found {len(response.cards)} cards:")
            for card in response.cards:
                print(f"  - {card.title} ({card.brand})")
                print(f"    NM ID: {card.nm_id}")
                print(f"    Vendor code: {card.vendor_code}")
        except Exception as e:
            print(f"Failed to get cards: {e}")
        print()

        # Get goods with prices
        print("Getting goods with prices...")
        try:
            goods = client.prices.get_goods_with_prices(limit=100)
            print(f"Found {len(goods)} goods with prices:")
            for good in goods:
                print(f"  - {good.vendor_code}: UPDATE₽ (-{good.discount}%)")
        except Exception as e:
            print(f"Failed to get prices: {e}")
        print()

        # Get seller balance
        print("Getting seller balance...")
        try:
            balance = client.finance.get_balance()
            print(f"  Currency: {balance.currency}")
            print(f"  Current: {balance.current}₽")
            print(f"  Available for withdrawal: {balance.for_withdraw}₽")
            print(f"  Blocked: {balance.blocked}₽ ({balance.blocked_percent:.1f}%)")
        except Exception as e:
            print(f"Failed to get balance: {e}")
        print()

        # Get sales summary (commented out - rate limit 1 req/min!)
        # from datetime import datetime, timedelta
        #
        # print("Getting sales summary...")
        # try:
        #     date_to = datetime.now()
        #     date_from = date_to - timedelta(days=7)
        #
        #     summary = client.statistics.get_sales_summary(
        #         date_from=date_from,
        #         date_to=date_to
        #     )
        #     print(f"  Total items: {summary.total_items}")
        #     print(f"  Quantity sold: {summary.quantity_sold}")
        #     print(f"  Revenue: {summary.revenue}₽")
        #     print(f"  To seller: {summary.to_seller}₽")
        #     print(f"  Commission: {summary.commission_percent:.1f}%")
        #     print(f"  Net: {summary.net_to_seller}₽")
        # except Exception as e:
        #     print(f"Failed to get sales summary: {e}")
        # print()

        # Example: Upload prices (commented out - requires valid data)
        # from wb_api.models.prices import Price
        #
        # print("Uploading prices...")
        # try:
        #     prices = [
        #         Price(nm_id=123456, price=1500, discount=20),
        #         Price(nm_id=123457, price=2000, discount=15),
        #     ]
        #     response = client.prices.upload_prices(prices)
        #     print(f"Task created: {response.task_id}")
        #
        #     # Wait for task completion with progress
        #     def show_progress(task):
        #         print(f"  Progress: {task.progress_percent:.1f}%")
        #
        #     result = client.prices.wait_for_task(
        #         response.task_id,
        #         on_progress=show_progress,
        #         timeout=60
        #     )
        #     print(f"  Completed: {result.processed_items}/{result.total_items}")
        # except Exception as e:
        #     print(f"Failed to upload prices: {e}")


if __name__ == "__main__":
    main()
