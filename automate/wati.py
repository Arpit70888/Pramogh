import requests
# from pramogh.settings import WATI_API_KEY

api_key = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI3MDhjYTJhOC04ZjVmLTQ3NTMtOGU5Mi01YTc5YjlmNzk5NjciLCJ1bmlxdWVfbmFtZSI6ImluZm9AcHJhbW9naC5jb20iLCJuYW1laWQiOiJpbmZvQHByYW1vZ2guY29tIiwiZW1haWwiOiJpbmZvQHByYW1vZ2guY29tIiwiYXV0aF90aW1lIjoiMDcvMjUvMjAyNCAwOTo0NzoxMiIsImRiX25hbWUiOiJtdC1wcm9kLVRlbmFudHMiLCJ0ZW5hbnRfaWQiOiI5MDA3IiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoiQURNSU5JU1RSQVRPUiIsImV4cCI6MjUzNDAyMzAwODAwLCJpc3MiOiJDbGFyZV9BSSIsImF1ZCI6IkNsYXJlX0FJIn0.UEDmf_XyWz1xYiTAhIQmbeaxamtpI-PFSoFldTLRa8A'
# api_key = f'Bearer {WATI_API_KEY}'


def get_chat(phone):
    url = f"https://live-mt-server.wati.io/9007/api/v1/getMessages/{phone}"
    headers = {
        "Authorization": f"{api_key}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response.json()


def get_contacts():
    url = "https://live-mt-server.wati.io/9007/api/v1/getContacts"
    headers = {
        "Authorization": f"{api_key}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response.json()


# tenant_info = get_chat(919557983049)
# print(tenant_info)

contacts = get_contacts()
print(contacts)
contact_list = contacts['contact_list']
print(contact_list[0]['phone'])
for contact in contact_list:
    phone = contact['phone']
    fullName = contact['fullName']
    print(f'{fullName} {phone}')
