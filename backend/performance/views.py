from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from .models import Performance
from .serializers import PerformanceSerializer, PerformanceSummarySerializer


class IsHROrOwnerReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow HR to create/update performance reviews,
    but allow employees to view their own reviews.
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.is_hr

    def has_object_permission(self, request, view, obj):
        # Read permissions for owner or HR
        if request.method in permissions.SAFE_METHODS:
            return obj.employee == request.user or request.user.is_hr
        # Write permissions only for HR
        return request.user.is_hr


class PerformanceListCreateView(generics.ListCreateAPIView):
    serializer_class = PerformanceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = []  # Temporarily disable permissions

    def get_queryset(self):
        return Performance.objects.all()  # Show all performance for testing

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)


class PerformanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PerformanceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsHROrOwnerReadOnly]

    def get_queryset(self):
        if self.request.user.is_hr:
            return Performance.objects.all()
        return Performance.objects.filter(employee=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def employee_performance_history(request, employee_id):
    """Get performance history for a specific employee."""
    # Check permissions
    if not request.user.is_hr and str(request.user.id) != str(employee_id):
        return Response(
            {'error': 'You can only view your own performance history'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    reviews = Performance.objects.filter(employee_id=employee_id).order_by('-review_date')
    serializer = PerformanceSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_performance_reviews(request):
    """Get all performance reviews for the current user."""
    reviews = Performance.objects.filter(employee=request.user).order_by('-review_date')
    serializer = PerformanceSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def performance_summary(request):
    """Get performance summary statistics."""
    if request.user.is_hr:
        # HR can see overall statistics
        total_reviews = Performance.objects.count()
        avg_rating = Performance.objects.aggregate(
            avg_rating=models.Avg('overall_rating')
        )['avg_rating'] or 0
        
        recent_reviews = Performance.objects.order_by('-created_at')[:5]
        
        summary = {
            'total_reviews': total_reviews,
            'average_rating': round(avg_rating, 2),
            'recent_reviews': PerformanceSummarySerializer(recent_reviews, many=True).data
        }
    else:
        # Employee can see their own statistics
        user_reviews = Performance.objects.filter(employee=request.user)
        total_reviews = user_reviews.count()
        
        if total_reviews > 0:
            avg_rating = user_reviews.aggregate(
                avg_rating=models.Avg('overall_rating')
            )['avg_rating']
            latest_review = user_reviews.order_by('-review_date').first()
        else:
            avg_rating = 0
            latest_review = None
        
        summary = {
            'total_reviews': total_reviews,
            'average_rating': round(avg_rating, 2) if avg_rating else 0,
            'latest_review': PerformanceSerializer(latest_review).data if latest_review else None
        }
    
    return Response(summary)


# Add the missing import
from django.db import models
