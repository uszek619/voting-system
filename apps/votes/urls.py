from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VoteViewSet, VoteOptionViewSet, UserVoteViewSet

router = DefaultRouter()
router.register(r'', VoteViewSet, basename='vote')
router.register(r'options', VoteOptionViewSet, basename='vote-option')
router.register(r'user-votes', UserVoteViewSet, basename='user-vote')

urlpatterns = [
    path('', include(router.urls)),
]