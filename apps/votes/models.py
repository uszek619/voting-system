from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Vote(models.Model):
    """Voting session"""
    VOTE_TYPE_CHOICES = (
        ('quorum', 'Quorum/Attendance'),
        ('regular', 'Regular Vote'),
        ('amendment', 'Amendment Vote'),
    )
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('archived', 'Archived'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='votes')
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    vote_type = models.CharField(max_length=20, choices=VOTE_TYPE_CHOICES, default='regular')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_votes')
    participants = models.ManyToManyField(User, related_name='participated_votes', blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'
    
    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


class VoteOption(models.Model):
    """Option for voting"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=500)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Vote Option'
        verbose_name_plural = 'Vote Options'
    
    def __str__(self):
        return self.text


class UserVote(models.Model):
    """Individual vote cast by user"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, related_name='user_votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_votes')
    vote_option = models.ForeignKey(VoteOption, on_delete=models.SET_NULL, null=True, related_name='votes')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('vote', 'user')
        verbose_name = 'User Vote'
        verbose_name_plural = 'User Votes'
    
    def __str__(self):
        return f"{self.user.email} - {self.vote.title}"