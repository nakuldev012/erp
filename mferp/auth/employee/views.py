from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework import mixins, generics
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .mixins import group_required
    
    
        
class EmployeelistView( generics.GenericAPIView,   mixins.ListModelMixin, ):
    serializer_class = EmployeeSerializer
    permission_class = [IsAuthenticated]
    queryset = Employee.objects.all()

    # group_required('hr_configuration')
    @group_required('hr_configuration')
    def get(self, request, *args, **kwargs):
        print(request.user)
        if not 'pk' in kwargs:
            return self.list(request)
        post = get_object_or_404(Employee, pk=kwargs['pk'])
        return Response(EmployeeSerializer(post).data, status=200)


    def post(self, request):
        data = request.data
        serializer = EmployeeSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(EmployeeSerializer(post).data, status=201)
        return Response(serializer.errors, status=400)

