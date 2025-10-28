from rest_framework import serializers
from .models import Payroll
from employees.models import Employee


class PayrollSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    generated_by_name = serializers.CharField(source='generated_by.full_name', read_only=True)
    employee_id = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Payroll
        fields = [
            'id', 'employee', 'employee_name', 'employee_id', 'month', 'year',
            'basic_salary', 'house_rent_allowance', 'medical_allowance',
            'transport_allowance', 'bonus', 'overtime_pay',
            'tax_deduction', 'provident_fund', 'insurance_deduction',
            'other_deductions', 'gross_salary', 'total_deductions',
            'net_salary', 'generated_date', 'generated_by', 'generated_by_name'
        ]
        read_only_fields = [
            'employee', 'gross_salary', 'total_deductions', 'net_salary',
            'generated_date', 'generated_by'
        ]

    def validate(self, data):
        """
        Convert employee_id to employee object before model validation
        """
        print(f"=== VALIDATE METHOD CALLED ===")
        print(f"Input data: {data}")
        employee_id = data.get('employee_id')
        print(f"Employee ID: {employee_id}")
        
        if employee_id:
            try:
                employee = Employee.objects.get(employee_id=employee_id)
                data['employee'] = employee
                print(f"Found employee: {employee.full_name}")
                print(f"Data after setting employee: {data}")
                # Set basic_salary from employee if not provided or is 0
                if not data.get('basic_salary') or data.get('basic_salary') == 0:
                    data['basic_salary'] = employee.salary
                    print(f"Set basic_salary from employee: {employee.salary}")
            except Employee.DoesNotExist:
                print(f"Employee with ID {employee_id} not found")
                raise serializers.ValidationError(f"Employee with ID {employee_id} not found")
        else:
            print("No employee_id found in data")
        
        # Validate month
        month = data.get('month')
        if month and (month < 1 or month > 12):
            raise serializers.ValidationError("Month must be between 1 and 12.")
        
        # Remove employee_id from validated data since it's not a model field
        data.pop('employee_id', None)
        print(f"Final data before return: {data}")
        print(f"=== END VALIDATE METHOD ===")
        return data


class PayrollSummarySerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)

    class Meta:
        model = Payroll
        fields = [
            'id', 'employee_name', 'month', 'year',
            'gross_salary', 'total_deductions', 'net_salary', 'generated_date'
        ]
