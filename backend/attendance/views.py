from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from datetime import date, timedelta
from .models import Attendance
from .serializers import AttendanceSerializer, AttendanceMarkSerializer


class AttendanceListCreateView(generics.ListCreateAPIView):
    serializer_class = AttendanceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = []  # Temporarily disable permissions

    def get_queryset(self):
        return Attendance.objects.all()  # Show all attendance for testing

    def perform_create(self, serializer):
        if self.request.user.is_hr:
            # HR can mark attendance for any employee
            serializer.save()
        else:
            # Employees can only mark their own attendance
            serializer.save(employee=self.request.user)


class AttendanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AttendanceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_hr:
            return Attendance.objects.all()
        return Attendance.objects.filter(employee=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_attendance(request):
    today = date.today()
    
    # Check if attendance already marked for today
    attendance_exists = Attendance.objects.filter(
        employee=request.user,
        date=today
    ).exists()
    
    if attendance_exists:
        return Response(
            {'error': 'Attendance already marked for today'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    data = request.data.copy()
    data['date'] = today
    
    serializer = AttendanceMarkSerializer(data=data)
    if serializer.is_valid():
        serializer.save(employee=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def monthly_attendance(request):
    month = request.GET.get('month', date.today().month)
    year = request.GET.get('year', date.today().year)
    
    try:
        month = int(month)
        year = int(year)
    except ValueError:
        return Response(
            {'error': 'Invalid month or year'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if request.user.is_hr:
        attendance_records = Attendance.objects.filter(
            date__month=month,
            date__year=year
        )
    else:
        attendance_records = Attendance.objects.filter(
            employee=request.user,
            date__month=month,
            date__year=year
        )
    
    serializer = AttendanceSerializer(attendance_records, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def attendance_summary(request):
    if not request.user.is_hr:
        # Employee summary
        employee = request.user
        current_month = date.today().month
        current_year = date.today().year
        
        monthly_records = Attendance.objects.filter(
            employee=employee,
            date__month=current_month,
            date__year=current_year
        )
        
        summary = {
            'employee': employee.full_name,
            'month': current_month,
            'year': current_year,
            'total_days': monthly_records.count(),
            'present_days': monthly_records.filter(status='Present').count(),
            'absent_days': monthly_records.filter(status='Absent').count(),
            'late_days': monthly_records.filter(status='Late').count(),
            'half_days': monthly_records.filter(status='Half Day').count(),
        }
        
        return Response(summary)
    
    else:
        # HR summary - overall statistics
        current_month = date.today().month
        current_year = date.today().year
        
        total_records = Attendance.objects.filter(
            date__month=current_month,
            date__year=current_year
        )
        
        summary = {
            'month': current_month,
            'year': current_year,
            'total_attendance_records': total_records.count(),
            'present_count': total_records.filter(status='Present').count(),
            'absent_count': total_records.filter(status='Absent').count(),
            'late_count': total_records.filter(status='Late').count(),
            'half_day_count': total_records.filter(status='Half Day').count(),
        }
        
        return Response(summary)
