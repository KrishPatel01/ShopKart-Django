from django.contrib import admin
from .models import Offer, Product, Checkout, Contact, ProductComment, ProductRating, Order

# Register your models here.

admin.site.register(Product)
admin.site.register(Checkout)
admin.site.register(Order)
admin.site.register(Contact)
admin.site.register(ProductComment)
admin.site.register(ProductRating)
admin.site.register(Offer)