from django.contrib import admin
from cart.models import Cart,Order,Account
# Register your models here.
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Account)