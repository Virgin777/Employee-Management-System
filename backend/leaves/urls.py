from django.urls import path
from . import views

urlpatterns = [
    path('', views.LeaveListCreateView.as_view(), name='leave-list-create'),
    path('<int:pk>/', views.LeaveDetailView.as_view(), name='leave-detail'),
    path('<int:pk>/approve-reject/', views.approve_reject_leave, name='approve-reject-leave'),
    path('pending/', views.pending_leaves, name='pending-leaves'),
]
