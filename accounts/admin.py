from django.contrib import admin

# Register your models here.
from accounts.models import CustomUser, PhoneOTP

admin.site.register(CustomUser)
admin.site.register(PhoneOTP)