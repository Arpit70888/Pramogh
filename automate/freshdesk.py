import json
import requests
from pramogh.settings import FRESHDESK_API_KEY

api_key = 'W9Gk-jRLKJ9_ykrWMEVUng'
api_key = FRESHDESK_API_KEY
url = 'https://pramogh.myfreshworks.com/crm/sales/api/contacts'

# Define headers with the API key for authentication
headers = {
    'Authorization': f'Token token={api_key}',
    'Content-Type': 'application/json'
}

# Define the contact data to be added
contact_data = {
    'contact': {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe2@example.com',
        'mobile_number': '1234567890'
        # Add any other fields as needed
    }
}

# Convert the contact data to JSON format
contact_data_json = json.dumps(contact_data)

# Make a POST request to add the contact
response = requests.post(url, headers=headers, data=contact_data_json)


# Check the response status code
if response.status_code == 201:
    print("Contact added successfully.")
    print("Response Data:", response.json())
elif response.status_code == 200:
    try:
        response_data = response.json()
        if 'contact' in response_data:
            print("Contact added successfully.")
            print("Response Data:", response_data)
        else:
            print("Request succeeded but the response does not contain expected data.")
    except json.JSONDecodeError:
        print("Request succeeded with status code 200, but response is not in JSON format.")
        print("Raw Response Content:", response.text)
elif response.status_code == 401:
    print("Authentication failed. API key is incorrect.")
else:
    print(f"Request failed with status code {response.status_code}")
    print("Response:", response.text)
