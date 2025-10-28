from django.contrib import admin
from .models import Performance


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'reviewer', 'review_period', 'review_date', 'overall_rating']
    list_filter = ['review_period', 'review_date', 'overall_rating']
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__employee_id']
    date_hierarchy = 'review_date'
    ordering = ['-review_date']
    
    fieldsets = (
        ('Review Information', {
            'fields': ('employee', 'reviewer', 'review_period', 'review_date')
        }),
        ('Ratings', {
            'fields': ('technical_skills', 'communication_skills', 'teamwork', 'leadership', 'problem_solving', 'punctuality', 'overall_rating')
        }),
        ('Feedback', {
            'fields': ('strengths', 'areas_for_improvement', 'goals_for_next_period', 'feedback')
        }),
    )
    
    readonly_fields = ['overall_rating']
