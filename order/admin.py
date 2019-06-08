from django.contrib import admin

from .models.person import Person
from .models.order import Order

admin.site.register(Person)
admin.site.register(Order)
