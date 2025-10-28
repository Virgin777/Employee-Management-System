from django.urls import path
from . import views

urlpatterns = [
    path('', views.PayrollListCreateView.as_view(), name='payroll-list-create'),
    path('<int:pk>/', views.PayrollDetailView.as_view(), name='payroll-detail'),
    path('<int:pk>/download/', views.download_payslip, name='payroll-download'),
    path('generate-bulk/', views.generate_bulk_payroll, name='generate-bulk-payroll'),
    path('employee/<int:employee_id>/<int:month>/<int:year>/', views.employee_payslip, name='employee-payslip'),
    path('my-payslips/', views.my_payslips, name='my-payslips'),
]
