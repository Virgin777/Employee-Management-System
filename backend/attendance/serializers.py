from rest_framework import serializers
from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)

    class Meta:
        model = Attendance
        fields = [
            'id', 'employee', 'employee_name', 'date', 'status',
            'check_in_time', 'check_out_time', 'working_hours', 'remarks',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['employee', 'created_at', 'updated_at']

    def validate(self, data):
        if data.get('check_in_time') and data.get('check_out_time'):
            if data['check_in_time'] >= data['check_out_time']:
                raise serializers.ValidationError("Check-out time must be after check-in time.")
        return data


class AttendanceMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['date', 'status', 'check_in_time', 'check_out_time', 'remarks']
