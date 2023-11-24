from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    HrConfigSerializer,
    
)
from rest_framework.permissions import IsAuthenticated
from .models import (
    HrConfig,
)

class EmployeeTypeUserAPIView(APIView):
    serializer_class = HrConfigSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest) -> Response:
        try:
            obj_employment_type = HrConfig.objects.get(label="Type Of Employment")

            queryset = HrConfig.objects.filter(parent=obj_employment_type)

            return Response(
                {
                    "data": HrConfigSerializer(queryset, many=True).data,
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            return Response(
                {
                    "message": "Something Went Wrong",
                    "success": False,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )