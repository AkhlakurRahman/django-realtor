from django.contrib import admin

from .models import Seller
# Register your models here.


class SellerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'hire_date')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'email')
    list_per_page = 25


admin.site.register(Seller, SellerAdmin)
