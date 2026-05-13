from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Vote, VoteOption, UserVote
from .serializers import (
    VoteSerializer, VoteOptionSerializer, UserVoteSerializer,
    CreateVoteSerializer, VoteResultsSerializer
)
from apps.users.views import IsAdminOrSuperAdmin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'vote_type', 'organization']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'start_time', 'end_time']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateVoteSerializer
        elif self.action == 'results':
            return VoteResultsSerializer
        return VoteSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'start', 'end']:
            return [IsAdminOrSuperAdmin()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'superadmin':
            return Vote.objects.all()
        elif user.role == 'admin':
            return Vote.objects.filter(organization=user.organization)
        else:
            return Vote.objects.filter(participants=user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def add_participants(self, request, pk=None):
        """Add participants to vote"""
        vote = self.get_object()
        user_ids = request.data.get('user_ids', [])
        
        for user_id in user_ids:
            from apps.users.models import CustomUser
            try:
                user = CustomUser.objects.get(id=user_id)
                vote.participants.add(user)
            except CustomUser.DoesNotExist:
                pass
        
        return Response({'message': 'Participants added'})
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Start the vote"""
        vote = self.get_object()
        vote.status = 'open'
        vote.start_time = timezone.now()
        vote.save()
        return Response({'message': 'Vote started'})
    
    @action(detail=True, methods=['post'])
    def end(self, request, pk=None):
        """End the vote"""
        vote = self.get_object()
        vote.status = 'closed'
        vote.end_time = timezone.now()
        vote.save()
        return Response({'message': 'Vote ended'})
    
    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """Get vote results"""
        vote = self.get_object()
        serializer = self.get_serializer(vote)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cast_vote(self, request, pk=None):
        """Cast a vote"""
        vote = self.get_object()
        
        if vote.status != 'open':
            return Response(
                {'detail': 'Vote is not open'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if request.user not in vote.participants.all():
            return Response(
                {'detail': 'You are not a participant'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if user already voted
        if UserVote.objects.filter(vote=vote, user=request.user).exists():
            return Response(
                {'detail': 'You have already voted'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        vote_option_id = request.data.get('vote_option_id')
        try:
            vote_option = VoteOption.objects.get(id=vote_option_id, vote=vote)
        except VoteOption.DoesNotExist:
            return Response(
                {'detail': 'Invalid option'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user_vote = UserVote.objects.create(
            vote=vote,
            user=request.user,
            vote_option=vote_option
        )
        
        serializer = UserVoteSerializer(user_vote)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VoteOptionViewSet(viewsets.ModelViewSet):
    queryset = VoteOption.objects.all()
    serializer_class = VoteOptionSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperAdmin]


class UserVoteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserVote.objects.all()
    serializer_class = UserVoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return UserVote.objects.filter(user=user)