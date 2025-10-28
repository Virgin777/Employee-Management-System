from django.urls import path
from . import views

urlpatterns = [
    path('', views.PerformanceListCreateView.as_view(), name='performance-list-create'),
    path('<int:pk>/', views.PerformanceDetailView.as_view(), name='performance-detail'),
    path('employee/<int:employee_id>/', views.employee_performance_history, name='employee-performance-history'),
    path('my-reviews/', views.my_performance_reviews, name='my-performance-reviews'),
    path('summary/', views.performance_summary, name='performance-summary'),
]
