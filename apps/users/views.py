from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser, UserBody, UserCadence
from .serializers import CustomUserSerializer, CreateUserSerializer, UserBodySerializer, UserCadenceSerializer
from django.contrib.auth import authenticate
import secrets
import string


class IsAdminOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.role in ['admin', 'superadmin'])


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'superadmin'


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT token view"""
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        
        try:
            user = CustomUser.objects.get(email=email)
            user_authenticated = authenticate(username=user.username, password=password)
            
            if user_authenticated:
                request.data['username'] = user.username
                return super().post(request, *args, **kwargs)
        except CustomUser.DoesNotExist:
            pass
        
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        return CustomUserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsAdminOrSuperAdmin()]
        if self.action in ['destroy', 'update', 'partial_update']:
            return [IsSuperAdmin()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'superadmin':
            return CustomUser.objects.all()
        elif user.role == 'admin':
            return CustomUser.objects.filter(organization=user.organization)
        else:
            return CustomUser.objects.filter(id=user.id)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user info"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        """Reset user password"""
        if not request.user.role == 'superadmin':
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        user = self.get_object()
        new_password = CustomUser.generate_password()
        user.set_password(new_password)
        user.save()
        
        return Response({
            'message': 'Password reset successfully',
            'new_password': new_password
        })


class UserBodyViewSet(viewsets.ModelViewSet):
    queryset = UserBody.objects.all()
    serializer_class = UserBodySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperAdmin]


class UserCadenceViewSet(viewsets.ModelViewSet):
    queryset = UserCadence.objects.all()
    serializer_class = UserCadenceSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperAdmin]