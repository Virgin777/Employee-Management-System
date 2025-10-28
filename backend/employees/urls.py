from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('token-login/', views.token_login_view, name='token-login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.EmployeeProfileView.as_view(), name='profile'),
    path('change-password/', views.change_password, name='change-password'),
    path('dashboard-stats/', views.dashboard_stats, name='dashboard-stats'),
    path('employee-ids/', views.get_employee_ids, name='employee-ids'),
    path('test/', views.TestEmployeeListView.as_view(), name='test-employee-list'),  # Test endpoint
    path('', views.EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
]
