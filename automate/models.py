from django.db import models


# Create your models here.
class Contact(models.Model):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20,blank=True, null=True)
    is_send = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    def __str__(self):
        return str(self.first_name)
