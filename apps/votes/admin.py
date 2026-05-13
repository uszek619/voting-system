from django.contrib import admin
from .models import Vote, VoteOption, UserVote

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'vote_type', 'status', 'start_time', 'end_time')
    list_filter = ('status', 'vote_type', 'organization', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(VoteOption)
class VoteOptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'vote', 'order')
    list_filter = ('vote',)
    search_fields = ('text', 'vote__title')


@admin.register(UserVote)
class UserVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'vote', 'vote_option', 'timestamp')
    list_filter = ('vote', 'timestamp')
    search_fields = ('user__email', 'vote__title')
    readonly_fields = ('timestamp',)