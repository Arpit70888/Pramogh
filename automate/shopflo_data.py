import datetime
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
        today_date = datetime.datetime.today().date()
        for order in orders:
            created_at_date = datetime.datetime.strptime(order['created_at'], "%Y-%m-%dT%H:%M:%S%z").date()
            if created_at_date == today_date:
                created_at = order['created_at']
                contact_email = order['contact_email']
                phone = order['phone']
                shipping_name = order.get('shipping_address', {}).get('name', 'No shipping name')
                fullName = shipping_name
                split_fullName = fullName.split(' ')
                if len(split_fullName) > 1:
                    first_name, last_name = fullName.split(' ', 1)
                else:
                    first_name = split_fullName[0]
                    last_name = None
                print(f"Created at: {created_at}, First_name: {first_name}, Last_name: {last_name}, Email: {contact_email}, Phone: {phone}")
        print(len(orders))


