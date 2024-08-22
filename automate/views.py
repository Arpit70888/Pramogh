import datetime

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
import json
from automate.freshdesk import freshDesk
from automate.models import Contact
from automate.serializers import ContactSerializers
from automate.wati import get_contacts
from rest_framework.response import Response


class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializers


class SyncDataFromWatiToFreshDesk(APIView):

    def post(self, request):
        contacts = get_contacts()
        contact_list = contacts['contact_list']
        today_date = datetime.datetime.today().date()
        for contact in contact_list:
            # only get the today's record from wati....................
            created_at_date = datetime.datetime.strptime(contact['created'], "%b-%d-%Y").date()
            print(created_at_date,today_date)
            if created_at_date == today_date:
                # split the name
                fullName = str(contact['fullName'])
                split_fullName = fullName.split(' ')
                if len(split_fullName) > 1:
                    first_name = split_fullName[0]
                    last_name = split_fullName[1:]
                else:
                    first_name = split_fullName[0]
                    last_name = None
                phone = contact['phone']

                email = f'{fullName}@gmail.com'
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

                break
        return Response("Done")
