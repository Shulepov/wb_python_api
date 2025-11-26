"""Example usage of Wildberries API SDK."""

from wb_api import WildberriesClient

# Replace with your actual API token
TOKEN = "your_api_token_here"


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
            response = client.content.get_cards(limit=5)
            print(f"Found {len(response.cards)} cards:")
            for card in response.cards:
                print(f"  - {card.title} ({card.brand})")
                print(f"    NM ID: {card.nm_id}")
                print(f"    Vendor code: {card.vendor_code}")
        except Exception as e:
            print(f"Failed to get cards: {e}")


if __name__ == "__main__":
    main()
