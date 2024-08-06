from django.contrib import admin
from accounts.models import *


# Register your models here.
@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'phone')


@admin.register(Otp)
class OTPModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'otp', 'type', 'verify')


@admin.register(Notification)
class OTPModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'messages')
