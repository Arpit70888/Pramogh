from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
# from django.utils.translation import ugettext as _
from django.db.models import signals
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib import messages

from accounts.choices import *


class ModelMixin(models.Model):
    """
        This mixins provide the default field in the models project wise
    """
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_created",
                                   on_delete=models.CASCADE, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_updated",
                                   on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=10, default='active', choices=STATUS_TYPE, help_text=('Status'))

    def __str__(self):
        return self.created_by.email

    class Meta:
        abstract = True


class Profile(ModelMixin):
    picture = models.FileField(upload_to='user/profile', null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=25, choices=GENDER, default='Male')

    def save(self, *args, **kwargs):
        if self.id is not None:
            return super(Profile, self).save()
        query = Profile.objects.filter(created_by=self.created_by)
        if len(query) <= 1:
            return super(Profile, self).save()
        raise ValueError("User already have Profile.")


class Otp(ModelMixin):
    otp = models.IntegerField(default=0)
    type = models.CharField(max_length=20, choices=OTP_TYPE, default='forgot', null=True, blank=True)
    verify = models.CharField(choices=OTP_VERIFY, default='false', max_length=100)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    messages = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.user


def notification_create(user, message):
    # get user instanse
    user = User.objects.get(pk=user.pk)

    # create notification
    notification = Notification(user=user, messages=message)
    notification.save()
    return True
