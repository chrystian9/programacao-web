from django.contrib import admin

from .models import *

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Payment)
admin.site.register(Address)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(Order)