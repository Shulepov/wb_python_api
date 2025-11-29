"""Example usage of Wildberries API SDK."""

import os
from datetime import datetime

from dotenv import load_dotenv

from wb_api import WildberriesClient

load_dotenv()

# Replace with your actual API token
TOKEN = os.getenv("API_TOKEN")

def get_token_info(client: WildberriesClient):
    token_info = client.token_info
    print(f"Seller ID: {token_info.seller_id}")
    print(f"Token type: {token_info.token_type}")
    print(f"Categories: {', '.join(token_info.categories)}")
    print(f"Expires at: {token_info.expires_at}")
    print()

def get_parent_categories(client: WildberriesClient):
    print("Getting parent categories...")
    try:
        categories = client.content.get_parent_categories()
        print(f"Found {len(categories)} categories:")
        for cat in categories[:5]:
            print(f"  - {cat.name} (ID: {cat.id})")
    except Exception as e:
        print(f"Failed to get categories: {e}")
    print()

def get_product_cards(client: WildberriesClient):
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

def get_goods_with_prices(client: WildberriesClient):
    print("Getting goods with prices...")
    try:
        goods = client.prices.get_goods_with_prices(limit=100)
        print(f"Found {len(goods)} goods with prices:")
        for good in goods:
            print(f"  - {good.vendor_code}: UPDATE₽ (-{good.discount}%)")
    except Exception as e:
        print(f"Failed to get prices: {e}")
    print()

def get_seller_balance(client: WildberriesClient):
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

def get_sales_summary(client: WildberriesClient):
    """Get sales summary (not implemented - use get_marketing_analytics instead)."""
    print("get_sales_summary is deprecated - use get_marketing_analytics instead")
    print()


def get_marketing_analytics(client: WildberriesClient):
    """Analyze marketing campaigns budget and expenses."""
    print("=== Marketing Analytics ===\n")

    try:
        # 1. Get current advertising balance
        print("Getting advertising balance...")
        balance = client.marketing.get_balance()
        print(f"  Current balance: {balance.balance:,.2f}₽")
        print(f"  Bonus balance: {balance.bonus:,.2f}₽")
        print(f"  Net balance: {balance.net:,.2f}₽")
        print()

        # 2. Get list of all campaigns
        print("Getting campaigns list...")
        campaigns_list = client.marketing.list_campaigns()
        adverts = campaigns_list.adverts
        print(f"  Total campaigns: {campaigns_list.all}")
        all_campaign_ids = []
        for advert in adverts:
            type = advert['type']
            status = advert['status']
            print(f'Type {type} status {status}')
            advert_list = advert['advert_list']
            for advert_item in advert_list:
                advertid = advert_item['advertId']
                print("\t", advertid)
                all_campaign_ids.append(advertid)
            print()


        if campaigns_list.all == 0:
            print("No campaigns found.")
            return

        # 3. Get detailed info for all campaigns (in batches of 100)
        print("Getting campaigns details...")
        campaigns_info = {}
        batch_size = 100
        for i in range(0, len(all_campaign_ids), batch_size):
            batch = all_campaign_ids[i:i + batch_size]
            try:
                batch_info = client.marketing.get_campaigns_info(batch)
                for camp in batch_info:
                    campaigns_info[camp.campaign_id] = {
                        "name": camp.name,
                        "type": camp.type,
                        "status": camp.status,
                        "budget": 0,
                        "spent": 0
                    }
            except Exception as e:
                print(f"  Warning: Failed to get info for batch: {e}")

        print(f"  Got details for {len(campaigns_info)} campaigns")
        print()

        # 4. Get expenses history from May 2025 to today
        print("Getting expenses history (May 2025 - today)...")
        date_to = datetime.now()
        date_from = datetime(2025, 11, 1)

        try:
            expenses = client.marketing.get_expenses_history(
                date_from=date_from,
                date_to=date_to
            )
            print(f"  Found {len(expenses)} expense records")
            print()

            # 5. Aggregate expenses by campaign
            for expense in expenses:
                campaign_id = expense.campaign_id
                if campaign_id in campaigns_info:
                    campaigns_info[campaign_id]["spent"] += expense.upd_sum

        except Exception as e:
            print(f"  Failed to get expenses history: {e}")
            print()

        # 6. Calculate total spent and display results
        print("=== Campaign Budget Analysis ===\n")

        total_spent = 0
        campaigns_with_expenses = []

        for campaign_id, info in campaigns_info.items():
            if info["spent"] > 0:
                campaigns_with_expenses.append((campaign_id, info))
                total_spent += info["spent"]

        # Sort by spent amount (descending)
        campaigns_with_expenses.sort(key=lambda x: x[1]["spent"], reverse=True)

        # Display each campaign
        print(f"{'ID':<12} {'Name':<30} {'Type':<8} {'Status':<10} {'Spent':>15}")
        print("-" * 80)

        for campaign_id, info in campaigns_with_expenses:
            print(
                f"{campaign_id:<12} "
                f"{info['name'][:28]:<30} "
                f"{info['type']:<8} "
                f"{info['status']:<10} "
                f"{info['spent']:>13,.2f}₽"
            )

        # Display summary
        print("-" * 80)
        print(f"{'TOTAL SPENT:':<62} {total_spent:>13,.2f}₽")
        print(f"{'CURRENT BALANCE:':<62} {balance.balance:>13,.2f}₽")
        print(f"{'TOTAL INVESTED (spent + balance):':<62} {total_spent + balance.balance:>13,.2f}₽")
        print()

        # Display campaigns without expenses
        campaigns_without_expenses = [
            (cid, info) for cid, info in campaigns_info.items()
            if info["spent"] == 0
        ]

        if campaigns_without_expenses:
            print(f"Campaigns without expenses: {len(campaigns_without_expenses)}")
            for campaign_id, info in campaigns_without_expenses[:5]:
                print(f"  - {info['name']} (ID: {campaign_id})")
            if len(campaigns_without_expenses) > 5:
                print(f"  ... and {len(campaigns_without_expenses) - 5} more")

    except Exception as e:
        print(f"Failed to get marketing analytics: {e}")
        import traceback
        traceback.print_exc()

    print()

def main():
    """Main example function."""
    # Initialize client
    with WildberriesClient(token=TOKEN, sandbox=False) as client:
        # Get token information
        get_token_info(client)

        # Check API connection
        print("Checking API connection...")
        try:
            status = client.ping()
            print(f"Ping successful: {status}")
        except Exception as e:
            print(f"Ping failed: {e}")
            return
        print()

        # Get parent categories
        #get_parent_categories(client)

        # Get product cards
        #get_product_cards(client)

        # Get goods with prices
        #get_goods_with_prices(client)

        # Get seller balance
        #get_seller_balance(client)

        # Get marketing analytics
        get_marketing_analytics(client)

        #get_sales_summary(client)

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
