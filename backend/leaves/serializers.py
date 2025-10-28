from rest_framework import serializers
from .models import Leave
from employees.serializers import EmployeeProfileSerializer


class LeaveSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.full_name', read_only=True)
    days_requested = serializers.ReadOnlyField()

    class Meta:
        model = Leave
        fields = [
            'id', 'employee', 'employee_name', 'leave_type', 'start_date', 
            'end_date', 'reason', 'status', 'approved_by', 'approved_by_name',
            'applied_date', 'response_date', 'hr_comments', 'days_requested'
        ]
        read_only_fields = ['employee', 'applied_date', 'approved_by', 'response_date']

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("End date must be after start date.")
        return data


class LeaveApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = ['status', 'hr_comments']

    def validate_status(self, value):
        if value not in ['Approved', 'Rejected']:
            raise serializers.ValidationError("Status must be either 'Approved' or 'Rejected'.")
        return value
