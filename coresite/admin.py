from django.contrib import admin
from .models import magog_sensor, magog_uhi

# Register your models here.
admin.site.register(magog_sensor)
admin.site.register(magog_uhi)
