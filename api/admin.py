from django.contrib import admin
from .models import ProviderProfile, Appointment, AvailableSlot

# Register your models here.
admin.site.register(ProviderProfile)
admin.site.register(Appointment)
admin.site.register(AvailableSlot)
