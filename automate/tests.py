from datetime import datetime
import requests

# Replace these with your actual values
SHOP_NAME = 'pramogh'  # Without .myshopify.com
ADMIN_API_ACCESS_TOKEN = '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'  # The Admin API access token


def get_orders():
    url = f'https://{SHOP_NAME}.myshopify.com/admin/api/2024-07/orders.json'  # Use the appropriate API version

    headers = {
        'X-Shopify-Access-Token': ADMIN_API_ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }

    orders = []
    params = {
        "limit": 250,  # Max limit for Shopify API
    }

    # Loop to handle pagination
    while url:
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            new_orders = data.get('orders', [])
            if new_orders:
                orders.extend(new_orders)

            # Check if there's a 'Link' header for pagination
            link_header = response.headers.get('Link')
            if link_header and 'rel="next"' in link_header:
                # Extract the next page URL from the Link header
                url = link_header.split(';')[0].strip('<>')
            else:
                url = None  # No more pages
        else:
            print(f'Error: {response.status_code} - {response.text}')
            return None

    return orders


if __name__ == '__main__':
    orders = get_orders()
    if orders:
        for order in orders:
            created_at = order['created_at']
            shipping_name = order.get('shipping_address', {}).get('name', 'No shipping name')
            print(f"Created at: {created_at}, Shipping name: {shipping_name}")
        print(len(orders))
