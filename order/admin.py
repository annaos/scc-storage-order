from django.contrib import admin

from django.contrib import admin

from .models import Person
from .models import Order

admin.site.register(Person)
admin.site.register(Order)
