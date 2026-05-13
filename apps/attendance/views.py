from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Attendance
from .serializers import AttendanceSerializer
from apps.users.views import IsAdminOrSuperAdmin
from django_filters.rest_framework import DjangoFilterBackend


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['meeting_date', 'is_present']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrSuperAdmin()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'superadmin':
            return Attendance.objects.all()
        elif user.role == 'admin':
            return Attendance.objects.filter(user__organization=user.organization)
        else:
            return Attendance.objects.filter(user=user)
    
    @action(detail=False, methods=['post'])
    def confirm_attendance(self, request):
        """User confirms their own attendance"""
        meeting_date = request.data.get('meeting_date')
        
        if not meeting_date:
            return Response({'detail': 'meeting_date is required'}, status=400)
        
        attendance, created = Attendance.objects.update_or_create(
            user=request.user,
            meeting_date=meeting_date,
            defaults={'is_present': True}
        )
        
        serializer = self.get_serializer(attendance)
        return Response(serializer.data)