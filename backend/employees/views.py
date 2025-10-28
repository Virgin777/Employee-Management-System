from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from .models import Employee
from .serializers import (
    EmployeeSerializer, EmployeeProfileSerializer, 
    LoginSerializer, ChangePasswordSerializer
)


class IsHROrReadOnly(permissions.BasePermission):
    """Custom permission to only allow HR to edit employees."""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.is_hr


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        # Create or get token for DRF Token authentication
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'token': token.key,  # DRF Token for alternative authentication
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'is_hr': user.is_hr,
                'employee_id': user.employee_id,
                'department': user.department,
                'designation': user.designation
            }
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def token_login_view(request):
    """Alternative login endpoint that returns only DRF Token"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Create or get token for DRF Token authentication
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'is_hr': user.is_hr,
                'employee_id': user.employee_id,
                'department': user.department,
                'designation': user.designation
            }
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_view(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = []  # Temporarily remove permission requirement

    def perform_create(self, serializer):
        # Generate employee ID
        last_employee = Employee.objects.order_by('id').last()
        if last_employee:
            last_id = int(last_employee.employee_id[3:])  # Remove 'EMP' prefix
            new_id = f"EMP{last_id + 1:04d}"
        else:
            new_id = "EMP0001"
        
        serializer.save(employee_id=new_id)


# Temporary test view without authentication
class TestEmployeeListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = []  # No authentication required
    authentication_classes = []


class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = []  # Temporarily disable permissions


class EmployeeProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = EmployeeProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = []  # Temporarily disable permissions

    def get_object(self):
        return self.request.user


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats(request):
    if request.user.is_hr:
        # HR Dashboard stats
        from leaves.models import Leave
        
        total_employees = Employee.objects.filter(is_active=True).count()
        pending_leaves = Leave.objects.filter(status='Pending').count()
        
        stats = {
            'total_employees': total_employees,
            'pending_leaves': pending_leaves,
            'user_type': 'HR'
        }
    else:
        # Employee Dashboard stats
        from leaves.models import Leave
        from attendance.models import Attendance
        from datetime import date, timedelta
        
        user_leaves = Leave.objects.filter(employee=request.user)
        this_month_attendance = Attendance.objects.filter(
            employee=request.user,
            date__month=date.today().month,
            date__year=date.today().year
        )
        
        stats = {
            'total_leaves_applied': user_leaves.count(),
            'pending_leaves': user_leaves.filter(status='Pending').count(),
            'this_month_attendance': this_month_attendance.count(),
            'user_type': 'Employee'
        }
    
    return Response(stats)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_employee_ids(request):
    """Get all employee IDs for dropdown selection."""
    employees = Employee.objects.filter(is_active=True).values('employee_id', 'first_name', 'last_name')
    employee_list = [
        {
            'employee_id': emp['employee_id'],
            'name': f"{emp['first_name']} {emp['last_name']}"
        }
        for emp in employees
    ]
    return Response(employee_list)
