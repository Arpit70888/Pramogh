from django.contrib import admin

# Register your models here.
from automate.models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'phone', 'is_send', 'created_at']
