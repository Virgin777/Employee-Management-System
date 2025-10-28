from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.utils import timezone
from .models import Leave
from .serializers import LeaveSerializer, LeaveApprovalSerializer


class LeaveListCreateView(generics.ListCreateAPIView):
    serializer_class = LeaveSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = []  # Temporarily disable permissions

    def get_queryset(self):
        return Leave.objects.all()  # Show all leaves for testing

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user)


class LeaveDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LeaveSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_hr:
            return Leave.objects.all()
        return Leave.objects.filter(employee=self.request.user)

    def update(self, request, *args, **kwargs):
        leave = self.get_object()
        
        # Only allow updates if leave is pending or user is HR
        if leave.status != 'Pending' and not request.user.is_hr:
            return Response(
                {'error': 'Cannot update approved/rejected leaves'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().update(request, *args, **kwargs)


@api_view(['PATCH'])
@permission_classes([])  # Temporarily disable permissions for testing
def approve_reject_leave(request, pk):
    # Manually check authentication
    from rest_framework.authtoken.models import Token
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if not auth_header or not auth_header.startswith('Token '):
        return Response(
            {'error': 'Authentication required'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    token_key = auth_header.split(' ')[1]
    try:
        token = Token.objects.get(key=token_key)
        user = token.user
    except Token.DoesNotExist:
        return Response(
            {'error': 'Invalid token'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    if not user.is_hr:
        return Response(
            {'error': 'Only HR can approve/reject leaves'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        leave = Leave.objects.get(pk=pk)
    except Leave.DoesNotExist:
        return Response(
            {'error': 'Leave not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    if leave.status != 'Pending':
        return Response(
            {'error': 'Leave has already been processed'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    serializer = LeaveApprovalSerializer(leave, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(
            approved_by=user,
            response_date=timezone.now()
        )
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def pending_leaves(request):
    if not request.user.is_hr:
        return Response(
            {'error': 'Only HR can view pending leaves'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    leaves = Leave.objects.filter(status='Pending')
    serializer = LeaveSerializer(leaves, many=True)
    return Response(serializer.data)
