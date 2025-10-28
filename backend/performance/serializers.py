from rest_framework import serializers
from .models import Performance


class PerformanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    reviewer_name = serializers.CharField(source='reviewer.full_name', read_only=True)

    class Meta:
        model = Performance
        fields = [
            'id', 'employee', 'employee_name', 'reviewer', 'reviewer_name',
            'review_period', 'review_date', 'technical_skills', 'communication_skills',
            'teamwork', 'leadership', 'problem_solving', 'punctuality',
            'overall_rating', 'strengths', 'areas_for_improvement',
            'goals_for_next_period', 'feedback', 'created_at', 'updated_at'
        ]
        read_only_fields = ['overall_rating', 'reviewer', 'created_at', 'updated_at']

    def validate(self, data):
        # Validate rating fields
        rating_fields = [
            'technical_skills', 'communication_skills', 'teamwork',
            'leadership', 'problem_solving', 'punctuality'
        ]
        
        for field in rating_fields:
            value = data.get(field)
            if value and (value < 1 or value > 5):
                raise serializers.ValidationError(f"{field} must be between 1 and 5.")
        
        return data


class PerformanceSummarySerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)

    class Meta:
        model = Performance
        fields = [
            'id', 'employee_name', 'review_period', 'review_date',
            'overall_rating', 'created_at'
        ]
