from rest_framework.serializers import ModelSerializer

from automate.models import Contact


class ContactSerializers(ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
