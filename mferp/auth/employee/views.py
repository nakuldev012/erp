# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .models import Employee
# from .serializers import EmployeeSerializer
# from rest_framework import mixins, generics
# from django.shortcuts import get_object_or_404
# from rest_framework.permissions import IsAuthenticated
# from .mixins import group_required
# from mferp.common.errors import ClientErrors, DatabaseErrors, UserErrors


# class EmployeelistView(
#     generics.GenericAPIView,
#     mixins.ListModelMixin,
# ):
#     serializer_class = EmployeeSerializer
#     permission_classes = [IsAuthenticated]
#     queryset = Employee.objects.all()

#     # group_required('hr_configuration')
#     # @group_required('hr_configuration')
#     def get(self, request, *args, **kwargs):
#         try:
#             if not "pk" in kwargs:
#                 return self.list(request)
#             post = get_object_or_404(Employee, pk=kwargs["pk"])
#             return Response(
#                 {
#                     "data": EmployeeSerializer(post).data,
#                     "success": True,
#                 },
#                 status=status.HTTP_200_OK,
#             )
#         except Exception as error:
#             return Response(
#                 {
#                     "message": "Something Went Wrong",
#                     "success": False,
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )

#     def post(self, request):
#         try:
#             data = request.data
#             serializer = EmployeeSerializer(data=data)
#             if serializer.is_valid():
#                 post = serializer.save()
#                 return Response(
#                     {
#                         "message": "Employee Successfully Created",
#                         "success": True,
#                     },
#                     status=status.HTTP_200_OK,
#                 )
#         except Exception as error:
#             return Response(
#                 {
#                     "message": "Something Went Wrong",
#                     "success": False,
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )
