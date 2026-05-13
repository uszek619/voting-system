from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
import uuid
import secrets
import string

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'Superadministrator'),
        ('admin', 'Administrator'),
        ('user', 'User'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    organization = models.ForeignKey(
        'organizations.Organization',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='users'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='created_users'
    )
    
    # ✅ DODAJ TE LINIE - FIX dla conflictów
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='customuser_set',  # Dodaj unique related_name
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_set',  # Dodaj unique related_name
        help_text='Specific permissions for this user.'
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
    
    @staticmethod
    def generate_password(length=12):
        """Generate secure random password"""
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(characters) for i in range(length))
    
    def is_superadmin(self):
        return self.role == 'superadmin'
    
    def is_admin(self):
        return self.role in ['admin', 'superadmin']
    
    def is_regular_user(self):
        return self.role == 'user'
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
    
    @staticmethod
    def generate_password(length=12):
        """Generate secure random password"""
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(characters) for i in range(length))
    
    def is_superadmin(self):
        return self.role == 'superadmin'
    
    def is_admin(self):
        return self.role in ['admin', 'superadmin']
    
    def is_regular_user(self):
        return self.role == 'user'


class UserBody(models.Model):
    """Association between users and organizational bodies"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bodies')
    body = models.ForeignKey('organizations.Body', on_delete=models.CASCADE, related_name='members')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'body')
        verbose_name = 'User Body'
        verbose_name_plural = 'User Bodies'
    
    def __str__(self):
        return f"{self.user.email} - {self.body.name}"


class UserCadence(models.Model):
    """Association between users and cadences"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cadences')
    cadence = models.ForeignKey('organizations.Cadence', on_delete=models.CASCADE, related_name='members')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'cadence')
        verbose_name = 'User Cadence'
        verbose_name_plural = 'User Cadences'
    
    def __str__(self):
        return f"{self.user.email} - {self.cadence.name}"