from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mferp.auth.user.models import Account
from mferp.address.models import Country, State, City
from mferp.upload.models import UploadedFile
from .serializers import AccountSerializer, BasicEmpSerializer, PersonalEmpSerializer
from mferp.mastertableconfig.models import MasterConfig
from rest_framework import generics, mixins
from mferp.common.errors import ClientErrors, DatabaseErrors, UserErrors
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import BasicEmpInfo, PrimaryEmpInfo, PersonalEmpInfo
from mferp.common.functions import get_date_datetime, get_string_datetime


class EmployeeTypeUserAPIView(APIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest) -> Response:
        try:
            user_type = request.query_params.get("user_type")
            if not user_type:
                raise ClientErrors("query parameter 'user_type' is required")
            obj_user_type = MasterConfig.objects.get(label=user_type)

            queryset = Account.objects.filter(user_type=obj_user_type)

            return Response(
                {
                    "data": AccountSerializer(queryset, many=True).data,
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )
        except UserErrors as error:
            return Response(
                {
                    "message": error.message,
                    "success": False,
                },
                status=error.response_code,
            )
        except Exception as error:
            return Response(
                {
                    "message": "Something Went Wrong",
                    "success": False,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class BasicEmployeeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        emp_id = request.query_params.get("emp_id")
        if not emp_id:
            raise ClientErrors("query parameter 'emp_id' is required")
        obj_emp = PrimaryEmpInfo.objects.get(id=emp_id)

        queryset = BasicEmpInfo.objects.filter(emp_id=obj_emp)

        return Response(
            {
                "data": BasicEmpSerializer(queryset, many=True).data,
                "success": True,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        try:
            data = request.data
            serializer = BasicEmpSerializer(data=data)
            if not serializer.is_valid(raise_exception=False):
                err = " ".join(
                    [
                        f"{field}: {', '.join(error)}"
                        for field, error in serializer.errors.items()
                    ]
                )
                raise ClientErrors(err)

            serializer.save()
            return Response(
                {"message": "Basic Employee is Successfully Created", "success": True},
                status=status.HTTP_201_CREATED,
            )
        except UserErrors as error:
            return Response(
                {
                    "message": error.message,
                    "success": False,
                },
                status=error.response_code,
            )
        except Exception as error:
            return Response(
                {
                    "message": "Something Went Wrong",
                    "success": False,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def patch(self, request, pk=None):
        try:
            instance = get_object_or_404(BasicEmpInfo, pk=pk)
            serializer = BasicEmpSerializer(instance, data=request.data, partial=True)
            if not serializer.is_valid(raise_exception=False):
                err = " ".join(
                    [
                        f"{field}: {', '.join(error)}"
                        for field, error in serializer.errors.items()
                    ]
                )
                raise ClientErrors(err)

            serializer.save()
            return Response(
                {"message": "Basic Employee is Successfully Updated", "success": True},
                status=status.HTTP_201_CREATED,
            )
        except UserErrors as error:
            return Response(
                {
                    "message": error.message,
                    "success": False,
                },
                status=error.response_code,
            )
        except Exception as error:
            return Response(
                {
                    "message": "Something Went Wrong",
                    "success": False,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PersonalEmployeeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        emp_id = request.query_params.get("emp_id")
        if not emp_id:
            raise ClientErrors("query parameter 'emp_id' is required")
        obj_emp = PrimaryEmpInfo.objects.get(id=emp_id)

        queryset = PersonalEmpInfo.objects.filter(emp_id=obj_emp)

        return Response(
            {
                "data": PersonalEmpSerializer(queryset, many=True).data,
                "success": True,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        try:
            data = request.data
            if ("profile_pic") not in request.data:
                    raise ClientErrors("profile_pic field is required")
            if ("character_certificate") not in request.data:
                raise ClientErrors("character_certificate field is required")
            if ("medical_certificate") not in request.data:
                raise ClientErrors("medical_certificate field is required")
            profile_pic = data.get("profile_pic")
            character_certificate = data.get("character_certificate")
            medical_certificate = data.get("medical_certificate")
            profile_pic_id = UploadedFile.objects.create(upload=profile_pic).id
            character_certificate_id = UploadedFile.objects.create(upload=character_certificate).id
            medical_certificate_id = UploadedFile.objects.create(upload=medical_certificate).id
            data["profile_pic"]=profile_pic_id
            data["character_certificate"]=character_certificate_id
            data["medical_certificate"]=medical_certificate_id
            
            serializer = PersonalEmpSerializer(data=data)
            if not serializer.is_valid(raise_exception=False):
                err = " ".join(
                    [
                        f"{field}: {', '.join(error)}"
                        for field, error in serializer.errors.items()
                    ]
                )
                raise ClientErrors(err)

            serializer.save()
            return Response(
                {"message": "Personal Employee is Successfully Created", "success": True},
                status=status.HTTP_201_CREATED,
            )
        except UserErrors as error:
            return Response(
                {
                    "message": error.message,
                    "success": False,
                },
                status=error.response_code,
            )
        except Exception as error:
            return Response(
                {
                    "message": "Something Went Wrong",
                    "success": False,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def patch(self, request, pk=None):
        try:
            instance = get_object_or_404(PersonalEmpInfo, pk=pk)
            serializer = PersonalEmpSerializer(instance, data=request.data, partial=True)
            if not serializer.is_valid(raise_exception=False):
                err = " ".join(
                    [
                        f"{field}: {', '.join(error)}"
                        for field, error in serializer.errors.items()
                    ]
                )
                raise ClientErrors(err)

            serializer.save()
            return Response(
                {"message": "Basic Employee is Successfully Updated", "success": True},
                status=status.HTTP_201_CREATED,
            )
        except UserErrors as error:
            return Response(
                {
                    "message": error.message,
                    "success": False,
                },
                status=error.response_code,
            )
        except Exception as error:
            return Response(
                {
                    "message": "Something Went Wrong",
                    "success": False,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

     