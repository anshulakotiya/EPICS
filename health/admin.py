from django.contrib import admin

# Register your models here.
from health.models import *
admin.site.register(User)
admin.site.register(HealthCard)
admin.site.register(doctorLicence)
admin.site.register(Documents)
admin.site.register(UserDisease)
