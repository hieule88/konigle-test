from django.contrib import admin
from .models import *

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ('email', 'is_active', 'is_superuser', 'is_staff')
admin.site.register(CustomUser, CustomUserAdmin)

class ShopOwnerAdmin(admin.ModelAdmin):
    model = ShopOwner
    list_display = ('user',)
admin.site.register(ShopOwner, ShopOwnerAdmin)

class CustomerEmailAdmin(admin.ModelAdmin):
    model = CustomerEmail
    list_display = ('email', 'created_date')
admin.site.register(CustomerEmail, CustomerEmailAdmin)
