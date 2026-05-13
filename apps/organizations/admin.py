from django.contrib import admin
from .models import Organization, Cadence, Body

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)


@admin.register(Cadence)
class CadenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'start_date', 'end_date', 'is_active')
    list_filter = ('organization', 'is_active', 'start_date')
    search_fields = ('name', 'organization__name')


@admin.register(Body)
class BodyAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'body_type', 'created_at')
    list_filter = ('body_type', 'organization', 'created_at')
    search_fields = ('name', 'organization__name')