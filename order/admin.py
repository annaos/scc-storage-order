from django.contrib import admin

from .models.person import Person
from .models.order import Order
from .models.personorder import PersonOrder

admin.site.register(Person)
admin.site.register(Order)
admin.site.register(PersonOrder)
