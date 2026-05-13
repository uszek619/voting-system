from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrganizationViewSet, CadenceViewSet, BodyViewSet

router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet, basename='organization')
router.register(r'cadences', CadenceViewSet, basename='cadence')
router.register(r'bodies', BodyViewSet, basename='body')

urlpatterns = [
    path('', include(router.urls)),
]