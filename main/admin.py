from django.contrib import admin
from .models import Categories, Callback, Product, MainSlider, links, CartItem

# Register your models here.
admin.site.register(Categories)
admin.site.register(Callback)
admin.site.register(Product)
admin.site.register(MainSlider)
admin.site.register(links)
admin.site.register(CartItem)