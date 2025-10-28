"""
URL configuration for employee_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse, HttpResponse

def api_root(request):
    """API root endpoint showing available endpoints"""
    if request.META.get('HTTP_ACCEPT', '').startswith('application/json'):
        # Return JSON for API clients
        return JsonResponse({
            'message': 'Employee Management System API',
            'endpoints': {
                'auth': '/api/auth/',
                'employees': '/api/employees/',
                'leaves': '/api/leaves/',
                'attendance': '/api/attendance/',
                'payroll': '/api/payroll/',
                'performance': '/api/performance/',
            }
        })
    else:
        # Return HTML for browser users
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Employee Management System API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
                .endpoint { background: #ecf0f1; padding: 10px; margin: 10px 0; border-radius: 4px; }
                .endpoint a { color: #2980b9; text-decoration: none; font-weight: bold; }
                .endpoint a:hover { text-decoration: underline; }
                .description { color: #7f8c8d; margin-top: 5px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Employee Management System API</h1>
                <p>Welcome to the Employee Management System REST API. Below are the available endpoints:</p>
                
                <div class="endpoint">
                    <a href="/api/auth/">/api/auth/</a>
                    <div class="description">Authentication endpoints (login, logout, profile)</div>
                </div>
                
                <div class="endpoint">
                    <a href="/api/employees/">/api/employees/</a>
                    <div class="description">Employee management endpoints</div>
                </div>
                
                <div class="endpoint">
                    <a href="/api/leaves/">/api/leaves/</a>
                    <div class="description">Leave management endpoints</div>
                </div>
                
                <div class="endpoint">
                    <a href="/api/attendance/">/api/attendance/</a>
                    <div class="description">Attendance tracking endpoints</div>
                </div>
                
                <div class="endpoint">
                    <a href="/api/payroll/">/api/payroll/</a>
                    <div class="description">Payroll management endpoints</div>
                </div>
                
                <div class="endpoint">
                    <a href="/api/performance/">/api/performance/</a>
                    <div class="description">Performance evaluation endpoints</div>
                </div>
                
                <p style="margin-top: 30px; color: #7f8c8d;">
                    <strong>Note:</strong> Most endpoints require authentication. 
                    Use the <a href="/api/auth/">/api/auth/</a> endpoints to obtain authentication tokens.
                </p>
            </div>
        </body>
        </html>
        """
        return HttpResponse(html)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),  # Root API endpoint
    path('api/auth/', include('employees.urls')),
    path('api/employees/', include('employees.urls')),
    path('api/leaves/', include('leaves.urls')),
    path('api/attendance/', include('attendance.urls')),
    path('api/payroll/', include('payroll.urls')),
    path('api/performance/', include('performance.urls')),
]
