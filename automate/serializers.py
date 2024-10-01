from rest_framework.serializers import ModelSerializer

from automate.models import Contact, ShopfloContact


class ContactSerializers(ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class ShopfloContactSerializers(ModelSerializer):
    class Meta:
        model = ShopfloContact
        fields = '__all__'
