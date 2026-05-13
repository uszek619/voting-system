from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Attendance(models.Model):
    """Meeting attendance record"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_records')
    meeting_date = models.DateField()
    is_present = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-meeting_date']
        unique_together = ('user', 'meeting_date')
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance'
    
    def __str__(self):
        return f"{self.user.email} - {self.meeting_date}"