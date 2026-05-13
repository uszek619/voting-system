from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, UserBody, UserCadence


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'organization', 'created_by')}),
    )
    list_display = ('email', 'username', 'role', 'organization', 'is_active', 'created_at')
    list_filter = ('role', 'organization', 'is_active', 'created_at')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-created_at',)


@admin.register(UserBody)
class UserBodyAdmin(admin.ModelAdmin):
    list_display = ('user', 'body', 'joined_at')
    list_filter = ('body', 'joined_at')
    search_fields = ('user__email', 'body__name')


@admin.register(UserCadence)
class UserCadenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'cadence', 'joined_at')
    list_filter = ('cadence', 'joined_at')
    search_fields = ('user__email', 'cadence__name')