from django.urls import path
from . import views

urlpatterns = [
    path('', views.AttendanceListCreateView.as_view(), name='attendance-list-create'),
    path('<int:pk>/', views.AttendanceDetailView.as_view(), name='attendance-detail'),
    path('mark/', views.mark_attendance, name='mark-attendance'),
    path('monthly/', views.monthly_attendance, name='monthly-attendance'),
    path('summary/', views.attendance_summary, name='attendance-summary'),
]
