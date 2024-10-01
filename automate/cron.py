import datetime
import json
from automate.freshdesk import freshDesk
from automate.models import Contact, ShopfloContact
from automate.shopflo_data import get_orders
from automate.wati import get_contacts
from rest_framework.response import Response


def SyncDataFromWatiToFreshDeskCronJob():
    contacts = get_contacts()
    contact_list = contacts['contact_list']
    today_date = datetime.datetime.today().date()
    for contact in contact_list:
        # only get the today's record from wati....................
        created_at_date = datetime.datetime.strptime(contact['created'], "%b-%d-%Y").date()
        print(created_at_date, today_date)
        if created_at_date == today_date:
            # split the name
            fullName = str(contact['fullName'])
            split_fullName = fullName.split(' ')
            if len(split_fullName) > 1:
                first_name, last_name = fullName.split(' ', 1)
            else:
                first_name = split_fullName[0]
                last_name = None
            phone = contact['phone']

            email = f'{phone}@wati.com'
            print(fullName, first_name, last_name, email, phone)
            # send or check from djagno db...................................
            filter_contact = Contact.objects.filter(first_name=first_name, last_name=last_name, phone=phone,
                                                    is_send=True)
            if not filter_contact:
                contact_create = Contact.objects.create(first_name=first_name, last_name=last_name, phone=phone)
                print("create contact")
                # send data into fresh desk..............................
                # Check the response status code
                response = freshDesk(first_name, last_name, email, phone)
                print("response", response)
                if response.status_code == 201:
                    print('201')
                    contact_create.is_send = True
                    contact_create.save()
                elif response.status_code == 200:
                    print('200')
                    try:
                        response_data = response.json()
                        if 'contact' in response_data:
                            contact_create.is_send = True
                            contact_create.save()

                    except json.JSONDecodeError:
                        print("Request succeeded with status code 200, but response is not in JSON format.")
                        print("Raw Response Content:", response.text)

                elif response.status_code == 401:
                    pass
                else:
                    print('duplicate')
                    contact_create.is_send = True
                    contact_create.save()

    return Response("Done")


def SyncDataFromShopfloToFreshDeskCronJob():
    shopflo_contacts = get_orders()
    if shopflo_contacts:
        today_date = datetime.datetime.today().date()
        for order in shopflo_contacts:
            created_at_date = datetime.datetime.strptime(order['created_at'], "%Y-%m-%dT%H:%M:%S%z").date()
            if created_at_date == today_date:
                created_at = order['created_at']
                contact_email = order['contact_email']
                phone = str(order['phone'])[-10:]
                if not phone:
                    phone = '0000000000'
                shipping_name = order.get('shipping_address', {}).get('name', 'No shipping name')
                fullName = shipping_name
                split_fullName = fullName.split(' ')
                if len(split_fullName) > 1:
                    first_name, last_name = fullName.split(' ', 1)
                else:
                    first_name = split_fullName[0]
                    last_name = None
                print(
                    f"Created at: {created_at}, First_name: {first_name}, Last_name: {last_name}, Email: {contact_email}, Phone: {phone}")

                filter_contact = ShopfloContact.objects.filter(first_name=first_name, last_name=last_name,
                                                               email=contact_email, phone=phone,
                                                               is_send=True)
                if not filter_contact:
                    ShopfloContact_create = ShopfloContact.objects.create(first_name=first_name,
                                                                          last_name=last_name,
                                                                          email=contact_email, phone=phone)

                    response = freshDesk(first_name, last_name, contact_email, phone)
                    print("response", response)
                    if response.status_code == 201:
                        print('201')
                        ShopfloContact_create.is_send = True
                        ShopfloContact_create.save()
                    elif response.status_code == 200:
                        print('200')
                        try:
                            response_data = response.json()
                            if 'contact' in response_data:
                                ShopfloContact_create.is_send = True
                                ShopfloContact_create.save()

                        except json.JSONDecodeError:
                            print("Request succeeded with status code 200, but response is not in JSON format.")
                            print("Raw Response Content:", response.text)

                    elif response.status_code == 401:
                        pass
                    else:
                        print('duplicate')
                        ShopfloContact_create.is_send = True
                        ShopfloContact_create.save()

    return Response("Done")