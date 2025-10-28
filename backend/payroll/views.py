from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.http import HttpResponse
from datetime import date
from .models import Payroll
from .serializers import PayrollSerializer, PayrollSummarySerializer
from employees.models import Employee


class IsHRPermission(permissions.BasePermission):
    """Custom permission for HR only operations."""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_hr


class PayrollListCreateView(generics.ListCreateAPIView):
    serializer_class = PayrollSerializer
    authentication_classes = [TokenAuthentication]
    
    def get_permissions(self):
        """
        Allow unauthenticated GET requests to view payroll data,
        but require HR authentication for POST requests.
        """
        if self.request.method == 'GET':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsHRPermission]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Payroll.objects.all()

    def post(self, request, *args, **kwargs):
        print(f"=== PAYROLL POST REQUEST ===")
        print(f"Request data: {request.data}")
        print(f"Request user: {request.user}")
        print(f"Is authenticated: {request.user.is_authenticated}")
        if hasattr(request.user, 'is_hr'):
            print(f"Is HR: {request.user.is_hr}")
        print(f"=== END PAYROLL DEBUG ===")
        
        try:
            response = super().post(request, *args, **kwargs)
            print(f"Response status: {response.status_code}")
            print(f"Response data: {response.data}")
            return response
        except Exception as e:
            print(f"Exception in post: {str(e)}")
            print(f"Exception type: {type(e)}")
            raise

    def perform_create(self, serializer):
        print(f"PayrollListCreateView.perform_create() called")
        print(f"Request data: {self.request.data}")
        print(f"User: {self.request.user}")
        print(f"User is_hr: {getattr(self.request.user, 'is_hr', 'No is_hr attribute')}")
        
        try:
            serializer.save(generated_by=self.request.user)
            print("Payroll saved successfully")
        except Exception as e:
            print(f"Error saving payroll: {str(e)}")
            raise

    def create(self, request, *args, **kwargs):
        print(f"=== CREATE METHOD CALLED ===")
        serializer = self.get_serializer(data=request.data)
        print(f"Serializer data: {request.data}")
        
        try:
            if serializer.is_valid():
                print("Serializer is valid, proceeding with save...")
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                print(f"Serializer validation errors: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Exception in create: {str(e)}")
            print(f"Exception type: {type(e)}")
            raise


class PayrollDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PayrollSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_hr:
            return Payroll.objects.all()
        return Payroll.objects.filter(employee=self.request.user)

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsHRPermission()]
        return [permissions.IsAuthenticated()]


@api_view(['POST'])
@permission_classes([IsHRPermission])
def generate_bulk_payroll(request):
    """Generate payroll for all employees for a specific month/year."""
    month = request.data.get('month')
    year = request.data.get('year')
    
    if not month or not year:
        return Response(
            {'error': 'Month and year are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        month = int(month)
        year = int(year)
    except ValueError:
        return Response(
            {'error': 'Invalid month or year'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if month < 1 or month > 12:
        return Response(
            {'error': 'Month must be between 1 and 12'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get all active employees
    employees = Employee.objects.filter(is_active=True)
    created_payrolls = []
    
    for employee in employees:
        # Check if payroll already exists
        existing_payroll = Payroll.objects.filter(
            employee=employee,
            month=month,
            year=year
        ).first()
        
        if not existing_payroll:
            # Create basic payroll record
            payroll = Payroll.objects.create(
                employee=employee,
                month=month,
                year=year,
                basic_salary=employee.salary,
                house_rent_allowance=employee.salary * 0.20,  # 20% of basic salary
                medical_allowance=1500,  # Fixed amount
                transport_allowance=1000,  # Fixed amount
                tax_deduction=employee.salary * 0.10,  # 10% tax
                provident_fund=employee.salary * 0.12,  # 12% PF
                generated_by=request.user
            )
            created_payrolls.append(payroll)
    
    serializer = PayrollSummarySerializer(created_payrolls, many=True)
    return Response({
        'message': f'Generated {len(created_payrolls)} payroll records',
        'payrolls': serializer.data
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def employee_payslip(request, employee_id, month, year):
    """Get specific payslip for an employee."""
    try:
        month = int(month)
        year = int(year)
    except ValueError:
        return Response(
            {'error': 'Invalid month or year'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check permissions
    if not request.user.is_hr and str(request.user.id) != str(employee_id):
        return Response(
            {'error': 'You can only view your own payslip'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        payroll = Payroll.objects.get(
            employee_id=employee_id,
            month=month,
            year=year
        )
    except Payroll.DoesNotExist:
        return Response(
            {'error': 'Payslip not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = PayrollSerializer(payroll)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_payslips(request):
    """Get all payslips for the current user."""
    payrolls = Payroll.objects.filter(employee=request.user).order_by('-year', '-month')
    serializer = PayrollSummarySerializer(payrolls, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def download_payslip(request, pk):
    """Download payslip as a formatted text file."""
    try:
        payroll = Payroll.objects.get(pk=pk)
    except Payroll.DoesNotExist:
        return Response(
            {'error': 'Payslip not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Check permissions - HR can download any, employees can only download their own
    if not request.user.is_hr and payroll.employee != request.user:
        return Response(
            {'error': 'You can only download your own payslip'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Generate payslip content
    content = f"""
===============================================
                PAYSLIP
===============================================

Employee: {payroll.employee.full_name} ({payroll.employee.employee_id})
Month/Year: {payroll.month}/{payroll.year}
Generated On: {payroll.generated_date.strftime('%Y-%m-%d %H:%M:%S')}
Generated By: {payroll.generated_by.full_name if payroll.generated_by else 'System'}

===============================================
                EARNINGS
===============================================

Basic Salary:           ${payroll.basic_salary:10.2f}
House Rent Allowance:   ${payroll.house_rent_allowance:10.2f}
Medical Allowance:      ${payroll.medical_allowance:10.2f}
Transport Allowance:    ${payroll.transport_allowance:10.2f}
Bonus:                  ${payroll.bonus:10.2f}
Overtime Pay:           ${payroll.overtime_pay:10.2f}

GROSS SALARY:           ${payroll.gross_salary:10.2f}

===============================================
                DEDUCTIONS
===============================================

Tax Deduction:          ${payroll.tax_deduction:10.2f}
Provident Fund:         ${payroll.provident_fund:10.2f}
Insurance Deduction:    ${payroll.insurance_deduction:10.2f}
Other Deductions:       ${payroll.other_deductions:10.2f}

TOTAL DEDUCTIONS:       ${payroll.total_deductions:10.2f}

===============================================
                SUMMARY
===============================================

Gross Salary:           ${payroll.gross_salary:10.2f}
Total Deductions:       ${payroll.total_deductions:10.2f}
NET SALARY:             ${payroll.net_salary:10.2f}

===============================================

This is a computer-generated payslip.
No signature is required.

===============================================
"""
    
    # Create HTTP response with the content
    response = HttpResponse(content, content_type='text/plain')
    filename = f"payslip_{payroll.employee.employee_id}_{payroll.month}_{payroll.year}.txt"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response
