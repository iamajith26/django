from django.contrib import admin
from .models import Product, ProductNew, Catergory

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductNew)
admin.site.register(Catergory)