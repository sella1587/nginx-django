from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from core.models import Ouvrage

@admin.register(Ouvrage)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'schema_name','code_client')
