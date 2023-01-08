from django.contrib import admin
from .models import Demand, Year, Geography, Skill
# Register your models here.

admin.site.register(Demand)
admin.site.register(Year)
admin.site.register(Geography)
admin.site.register(Skill)

