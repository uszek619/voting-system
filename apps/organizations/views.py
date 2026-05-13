from rest_framework import viewsets, permissions
from .models import Organization, Cadence, Body
from .serializers import OrganizationSerializer, CadenceSerializer, BodySerializer
from apps.users.views import IsSuperAdmin, IsAdminOrSuperAdmin


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperAdmin]


class CadenceViewSet(viewsets.ModelViewSet):
    queryset = Cadence.objects.all()
    serializer_class = CadenceSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperAdmin]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'superadmin':
            return Cadence.objects.all()
        elif user.role == 'admin':
            return Cadence.objects.filter(organization=user.organization)
        else:
            return Cadence.objects.filter(organization__users=user)


class BodyViewSet(viewsets.ModelViewSet):
    queryset = Body.objects.all()
    serializer_class = BodySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperAdmin]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'superadmin':
            return Body.objects.all()
        elif user.role == 'admin':
            return Body.objects.filter(organization=user.organization)
        else:
            return Body.objects.filter(organization__users=user)