from rest_framework import serializers
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Attendance
        fields = ['id', 'user', 'user_email', 'meeting_date', 'is_present', 'note', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']