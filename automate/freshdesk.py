import json
import requests

# from pramogh.settings import FRESHDESK_API_KEY

api_key = 'W9Gk-jRLKJ9_ykrWMEVUng'
# api_key = FRESHDESK_API_KEY
# url = 'https://pramogh.myfreshworks.com/crm/sales/api/contacts/402093165732'
url = 'https://pramogh.myfreshworks.com/crm/sales/api/contacts'

# Define headers with the API key for authentication
headers = {
    'Authorization': f'Token token={api_key}',
    'Content-Type': 'application/json'
}


def freshDesk(first_name, last_name, email, phone):
    contact_data = {
        'contact': {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'mobile_number': phone,
            'first_source': 'WhatsApp Chat',
            'last_source': 'WhatsApp Chat',
            'tags': 'WhatsApp Chat',
        }
    }
    contact_data_json = json.dumps(contact_data)

    # Make a POST request to add the contact
    response = requests.post(url, headers=headers, data=contact_data_json)

    return response


#
# freshDesk_res = freshDesk('Arpit', 'gupta', 'arpit1@gmail.com', '7088851096')
# print(freshDesk_res)


def getContact():
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        contacts = response.json()
        print("Contacts retrieved successfully:")
        return contacts
    else:
        print(f"Failed to retrieve contacts. Status code: {response.status_code}")
        return response.text


# print(getContact())
