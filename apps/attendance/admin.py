from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'meeting_date', 'is_present', 'created_at')
    list_filter = ('is_present', 'meeting_date', 'created_at')
    search_fields = ('user__email', 'note')
    readonly_fields = ('created_at', 'updated_at')