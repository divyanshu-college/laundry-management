from django.contrib import admin
from .models import LaundryBooking, LaundryItem


admin.site.register(LaundryBooking)
admin.site.register(LaundryItem)