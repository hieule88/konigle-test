from django.contrib import admin
from .models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_superuser', 'is_staff', 'date_joined']
admin.site.register(User, UserAdmin)

class VisitorEmailAdmin(admin.ModelAdmin):
    model = VisitorEmail
    list_display = ['email', 'status', 'created_at']
admin.site.register(VisitorEmail, VisitorEmailAdmin)

class SellerAdmin(admin.ModelAdmin):
    model = Seller
    list_display = ['user', 'is_email_sent', 'created_at']
admin.site.register(Seller, SellerAdmin)
