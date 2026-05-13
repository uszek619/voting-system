from rest_framework import serializers
from .models import Vote, VoteOption, UserVote

class VoteOptionSerializer(serializers.ModelSerializer):
    vote_count = serializers.SerializerMethodField()
    
    class Meta:
        model = VoteOption
        fields = ['id', 'text', 'order', 'vote_count']
        read_only_fields = ['id', 'vote_count']
    
    def get_vote_count(self, obj):
        return obj.votes.count()


class VoteSerializer(serializers.ModelSerializer):
    options = VoteOptionSerializer(many=True, read_only=True)
    participants_count = serializers.SerializerMethodField()
    voted_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Vote
        fields = [
            'id', 'organization', 'title', 'description', 'vote_type',
            'status', 'created_by', 'participants_count', 'voted_count',
            'start_time', 'end_time', 'is_anonymous', 'options',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
    
    def get_participants_count(self, obj):
        return obj.participants.count()
    
    def get_voted_count(self, obj):
        return obj.user_votes.count()


class CreateVoteSerializer(serializers.ModelSerializer):
    options = serializers.ListField(child=serializers.CharField(), write_only=True)
    
    class Meta:
        model = Vote
        fields = [
            'title', 'description', 'vote_type', 'is_anonymous',
            'organization', 'options'
        ]
    
    def create(self, validated_data):
        options = validated_data.pop('options')
        vote = Vote.objects.create(**validated_data)
        vote.created_by = self.context['request'].user
        vote.save()
        
        for i, option_text in enumerate(options):
            VoteOption.objects.create(vote=vote, text=option_text, order=i)
        
        return vote


class UserVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVote
        fields = ['id', 'vote', 'user', 'vote_option', 'timestamp']
        read_only_fields = ['id', 'user', 'timestamp']


class VoteResultsSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    total_votes = serializers.SerializerMethodField()
    participation_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = Vote
        fields = [
            'id', 'title', 'vote_type', 'status', 'total_votes',
            'participation_rate', 'options', 'created_at', 'end_time'
        ]
    
    def get_options(self, obj):
        options_data = []
        for option in obj.options.all():
            vote_count = option.votes.count()
            options_data.append({
                'id': option.id,
                'text': option.text,
                'votes': vote_count,
                'percentage': (vote_count / obj.user_votes.count() * 100) if obj.user_votes.count() > 0 else 0
            })
        return options_data
    
    def get_total_votes(self, obj):
        return obj.user_votes.count()
    
    def get_participation_rate(self, obj):
        if obj.participants.count() == 0:
            return 0
        return (obj.user_votes.count() / obj.participants.count()) * 100