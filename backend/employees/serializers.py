from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Employee
        fields = [
            'id', 'employee_id', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'department', 'designation', 'date_of_joining', 'salary',
            'is_hr', 'is_active', 'password', 'date_created'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'salary': {'write_only': True},  # Only HR can see salary
            'employee_id': {'read_only': True},  # Auto-generated, should not be provided by user
            'email': {'required': False}  # Not required for updates
        }

    def validate(self, data):
        # For create operations, email and password are required
        if not self.instance:  # Creating new employee
            if not data.get('email'):
                raise serializers.ValidationError({'email': 'This field is required for new employees.'})
            if not data.get('password'):
                raise serializers.ValidationError({'password': 'This field is required for new employees.'})
        
        # For updates, email changes are not allowed to prevent unique constraint issues
        if self.instance and 'email' in data:
            if data['email'] != self.instance.email:
                raise serializers.ValidationError({'email': 'Email cannot be changed after creation.'})
        
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        employee = Employee(**validated_data)
        employee.set_password(password)
        employee.save()
        return employee

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance


class EmployeeProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Employee
        fields = [
            'id', 'employee_id', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'department', 'designation', 'date_of_joining', 'date_created'
        ]
        read_only_fields = ['employee_id', 'email', 'date_of_joining', 'date_created']


class LoginSerializer(serializers.Serializer):
    email_or_employee_id = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email_or_employee_id = data.get('email_or_employee_id')
        password = data.get('password')

        if email_or_employee_id and password:
            # Try to find user by email first, then by employee_id
            user = None
            
            # Check if it's an email format
            if '@' in email_or_employee_id:
                try:
                    user = Employee.objects.get(email=email_or_employee_id)
                except Employee.DoesNotExist:
                    pass
            else:
                # Try to find by employee_id
                try:
                    user = Employee.objects.get(employee_id=email_or_employee_id)
                except Employee.DoesNotExist:
                    pass
            
            if user and user.check_password(password):
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError('Account is disabled.')
            else:
                raise serializers.ValidationError('Invalid email/employee ID or password.')
        else:
            raise serializers.ValidationError('Must include email/employee ID and password.')

        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect.')
        return value
