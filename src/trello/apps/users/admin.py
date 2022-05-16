from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, OTPRequest


@admin.register(User)
class AppUserAdmin(UserAdmin):
    pass


@admin.register(OTPRequest)
class OTPRequestAdmin(admin.ModelAdmin):
    list_display = ('request_id', 'channel', 'receiver', 'password', 'created')
