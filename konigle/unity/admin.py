from django.contrib import admin
from .models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_superuser', 'is_staff', 'date_joined']
admin.site.register(User, UserAdmin)

class ShopOwnerAdmin(admin.ModelAdmin):
    model = ShopOwner
    list_display = ['user', 'created_date']
admin.site.register(ShopOwner, ShopOwnerAdmin)

class CustomerEmailAdmin(admin.ModelAdmin):
    model = CustomerEmail
    list_display = ['email', 'created_date']
admin.site.register(CustomerEmail, CustomerEmailAdmin)
