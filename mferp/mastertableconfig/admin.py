from django.contrib import admin
from .models import (
    MasterConfig,Organization,OrgAddress,Test
)

admin.site.register(MasterConfig)
admin.site.register(Organization)
admin.site.register(OrgAddress)
admin.site.register(Test)