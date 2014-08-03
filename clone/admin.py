from django.contrib import admin

from clone.models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('username', 'title', 'description', 'currency', 'base_price',
                    'date_added', 'url', 'sold')

admin.site.register(Product, ProductAdmin)
