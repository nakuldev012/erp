from django.contrib import admin
from .models import (
    MasterConfig,Organization
)

admin.site.register(MasterConfig)
admin.site.register(Organization)