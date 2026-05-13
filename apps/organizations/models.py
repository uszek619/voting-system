from django.db import models
import uuid

class Organization(models.Model):
    """Youth council or organization"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
    
    def __str__(self):
        return self.name


class Cadence(models.Model):
    """Council term/session"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='cadences')
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ('organization', 'name')
        verbose_name = 'Cadence'
        verbose_name_plural = 'Cadences'
    
    def __str__(self):
        return f"{self.organization.name} - {self.name}"


class Body(models.Model):
    """Organizational body (board, commission, etc.)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='bodies')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    body_type = models.CharField(
        max_length=50,
        choices=[
            ('board', 'Board'),
            ('committee', 'Committee'),
            ('revision', 'Revision Commission'),
            ('other', 'Other'),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ('organization', 'name')
        verbose_name = 'Body'
        verbose_name_plural = 'Bodies'
    
    def __str__(self):
        return f"{self.organization.name} - {self.name}"