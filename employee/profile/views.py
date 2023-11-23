from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mferp.auth.user.models import Account
from mferp.address.models import Country, State, City
from mferp.upload.models import UploadedFile
from .serializers import (
    AccountSerializer,
    BasicEmpSerializer,
    PersonalEmpSerializer,
    AccountEmpSerializer,
    AddressEmpSerializer,
    PrimaryEmpInfoSerializer,
)
from mferp.mastertableconfig.models import MasterConfig
from rest_framework import generics, mixins
from mferp.common.errors import ClientErrors, DatabaseErrors, UserErrors
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import (
    BasicEmpInfo,
    PrimaryEmpInfo,
    PersonalEmpInfo,
    AccountEmpInfo,
    AddressEmpInfo,
)
from mferp.common.functions import get_date_datetime, get_string_datetime
import django.core.files.uploadedfile


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


class PrimaryEmpInfoView(generics.GenericAPIView):
    queryset = PrimaryEmpInfo.objects.all()
    serializer_class = PrimaryEmpInfoSerializer
    
    def post(self, request):
            # import ipdb;
            # ipdb.set_trace()
            try:
                account_id = request.data.get('user_id')  
                account_instance = Account.objects.get(id=account_id)
                request.data['user_id'] = account_instance.id
                serializer=PrimaryEmpInfoSerializer(data=request.data)
                if not serializer.is_valid(raise_exception=False):
                    err = ""
                    for field, error in serializer.errors.items():
                        err += "{}: {} ".format(field, ",".join(error))
                    raise ClientErrors(err)

                emp = serializer.save()
                primary_emp_info_id = emp.id
                return Response(
                    {
                        "emp_id":primary_emp_info_id,
                        "message": "Primary information for the employee has been saved",
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


    def get(self, request,*args, **kwargs):
        # import ipdb;
        # ipdb.set_trace()
        user_id = request.query_params.get('user_id')
        
        if user_id:
            try:
                emp = PrimaryEmpInfo.objects.get(user_id_id=user_id)
                serializer = PrimaryEmpInfoSerializer(emp)
                return Response(
                {
                "data": serializer.data,
                "success": True,
            },
            status=status.HTTP_200_OK,
        )
            except PrimaryEmpInfo.DoesNotExist:
                return Response(
                {
                "message": "Primary information for given user not found",
                "success": False,
            },
            status=status.HTTP_404_NOT_FOUND,
        )
        else:
            return Response(
                    {
                    "message": "User id not provided",
                    "success": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
    
    def put(self, request, pk=None, *args, **kwargs):
        id=pk
        if id is not None:
            try:
                emp = PrimaryEmpInfo.objects.get(id=id)
            except PrimaryEmpInfo.DoesNotExist:
                return Response(
                {
                "message": "Primary information for given user not found",
                "success": False,
            },
            status=status.HTTP_404_NOT_FOUND,
            )
            serializer = PrimaryEmpInfoSerializer(emp, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": "Primary information for the given user has been updated",
                        "success": True,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "message": "Invalid data provided",
                        "errors": serializer.errors,
                        "success": False,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                    {
                    "message": "Employee id is not valid",
                    "success": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
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

    def put(self, request, pk=None):
        try:
            obj_emp = PrimaryEmpInfo.objects.get(id=pk)
            pk = obj_emp.id
            account_emp_info = BasicEmpInfo.objects.get(emp_id__id=pk)
            if not account_emp_info:
                raise ClientErrors("Basic Information is not created for this employee")
            serializer = BasicEmpSerializer(account_emp_info, data=request.data)
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
            profile_pic = data.get("profile_pic", "")
            character_certificate = data.get("character_certificate", "")
            medical_certificate = data.get("medical_certificate", "")
            created_by = request.user
            profile_pic_id = UploadedFile.objects.create(
                upload=profile_pic, created_by=created_by
            ).id
            character_certificate_id = UploadedFile.objects.create(
                upload=character_certificate, created_by=created_by
            ).id
            medical_certificate_id = UploadedFile.objects.create(
                upload=medical_certificate, created_by=created_by
            ).id
            data["profile_pic"] = profile_pic_id
            data["character_certificate"] = character_certificate_id
            data["medical_certificate"] = medical_certificate_id

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
                {
                    "message": "Personal Employee is Successfully Created",
                    "success": True,
                },
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

    def put(self, request, pk=None):
        try:
            data = request.data
            mutable_data = request.data.copy()
            if not pk:
                raise ClientErrors("pk is required")

            obj_emp = PrimaryEmpInfo.objects.get(id=pk)
            instance = get_object_or_404(PersonalEmpInfo, emp_id=obj_emp)
            profile_pic = data.get("profile_pic", "")
            character_certificate = data.get("character_certificate", "")
            medical_certificate = data.get("medical_certificate", "")
            created_by = request.user
            if not isinstance(profile_pic, str):
                profile_pic_instance = instance.profile_pic
                profile_pic_instance.upload = profile_pic
                profile_pic_instance.created_by = created_by
                profile_pic_instance.save()
                profile_pic_id = profile_pic_instance.id
                mutable_data["profile_pic"] = profile_pic_id
            else:
                profile_pic_instance = instance.profile_pic
                profile_pic_id = profile_pic_instance.id
                mutable_data["profile_pic"] = profile_pic_id

            if not isinstance(profile_pic, str):
                character_certificate_instance = instance.character_certificate
                character_certificate_instance.upload = character_certificate
                character_certificate_instance.created_by = created_by
                character_certificate_instance.save()
                character_certificate_id = character_certificate_instance.id
                mutable_data["character_certificate"] = character_certificate_id

            else:
                character_certificate_instance = instance.character_certificate
                character_certificate_id = character_certificate_instance.id
                mutable_data["character_certificate"] = character_certificate_id

            if not isinstance(profile_pic, str):
                medical_certificate_instance = instance.medical_certificate
                medical_certificate_instance.upload = medical_certificate
                medical_certificate_instance.created_by = created_by
                medical_certificate_instance.save()
                medical_certificate_id = medical_certificate_instance.id
                mutable_data["medical_certificate"] = medical_certificate_id
            else:
                medical_certificate_instance = instance.medical_certificate
                medical_certificate_id = medical_certificate_instance.id
                mutable_data["medical_certificate"] = medical_certificate_id

            serializer = PersonalEmpSerializer(instance, data=mutable_data)
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
                {
                    "message": "Personal Employee is Successfully Updated",
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


class AccountEmployeeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        emp_id = request.query_params.get("emp_id")
        if not emp_id:
            raise ClientErrors("query parameter 'emp_id' is required")
        obj_emp = PrimaryEmpInfo.objects.get(id=emp_id)

        queryset = AccountEmpInfo.objects.filter(emp_id=obj_emp)

        return Response(
            {
                "data": AccountEmpSerializer(queryset, many=True).data,
                "success": True,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        try:
            data = request.data
            serializer = AccountEmpSerializer(data=data)
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
                {
                    "message": "Employee Account is Successfully Created",
                    "success": True,
                },
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

    def put(self, request, pk=None):
        try:
            obj_emp = PrimaryEmpInfo.objects.get(id=pk)
            pk = obj_emp.id
            account_emp_info = AccountEmpInfo.objects.get(emp_id__id=pk)
            if not account_emp_info:
                raise ClientErrors("Account is not created for this employee")
            serializer = AccountEmpSerializer(account_emp_info, data=request.data)
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
                {
                    "message": "Employee Account is Successfully Updated",
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


class AddressEmployeeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        emp_id = request.query_params.get("emp_id")
        if not emp_id:
            raise ClientErrors("query parameter 'emp_id' is required")
        obj_emp = PrimaryEmpInfo.objects.get(id=emp_id)

        queryset = AddressEmpInfo.objects.filter(emp=obj_emp)

        return Response(
            {
                "data": AddressEmpSerializer(queryset, many=True).data,
                "success": True,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        try:
            data = request.data
            # seen={}
            if ("permanent_address") not in request.data:
                raise ClientErrors("permanent address field is required")
            if ("correspondence_address") not in request.data:
                raise ClientErrors("correspondence address field is required")
            if ("permanent_pin_code") not in request.data:
                raise ClientErrors("permanent pin code field is required")
            if ("correspondence_pin_code") not in request.data:
                raise ClientErrors("correspondence pin code field is required")
            if ("permanent_city") not in request.data:
                raise ClientErrors("permanent city field is required")
            if ("correspondence_city") not in request.data:
                raise ClientErrors("correspondence city field is required")
            if ("is_both_address_same") not in request.data:
                raise ClientErrors("is_both_address_same field is required")
            if ("emp_id") not in request.data:
                raise ClientErrors("emp field is required")
            if ("isVerified") not in request.data:
                raise ClientErrors("isVerified field is required")
            if ("permanent_address_proof") not in request.data:
                raise ClientErrors("permanent address proof field is required")
            if ("correspondence_address_proof") not in request.data:
                raise ClientErrors("correspondence address proof field is required")
            permanent_address_proof = data.get("permanent_address_proof")
            permanent_address = data.get("permanent_address")
            permanent_landmark = data.get("permanent_landmark")
            permanent_city = data.get("permanent_city")
            permanent_pin_code = data.get("permanent_pin_code")
            correspondence_address_proof = data.get("correspondence_address_proof")
            correspondence_address = data.get("correspondence_address")
            correspondence_landmark = data.get("correspondence_landmark")
            correspondence_city = data.get("correspondence_city")
            correspondence_pin_code = data.get("correspondence_pin_code")
            is_both_address_same = data.get("is_both_address_same")
            emp_id = data.get("emp_id")
            isVerified = data.get("isVerified")
            created_by = request.user
            permanent_city_instance = City.objects.get(pk=permanent_city)
            correspondence_city_instance = City.objects.get(pk=correspondence_city)
            permanent_address_proof_instance = UploadedFile.objects.create(
                upload=permanent_address_proof, created_by=created_by
            )
            correspondence_address_proof_instance = UploadedFile.objects.create(
                upload=correspondence_address_proof, created_by=created_by
            )
            emp_instance = PrimaryEmpInfo.objects.get(id=emp_id)
            AddressEmpInfo.objects.create(
                address_proof=permanent_address_proof_instance,
                emp=emp_instance,
                isVerified=isVerified,
                is_both_address_same=is_both_address_same,
                type="permanent",
                address=permanent_address,
                landmark=permanent_landmark,
                city=permanent_city_instance,
                zip=permanent_pin_code,
            )
            AddressEmpInfo.objects.create(
                address_proof=correspondence_address_proof_instance,
                emp=emp_instance,
                isVerified=isVerified,
                is_both_address_same=is_both_address_same,
                type="correspondence",
                address=correspondence_address,
                landmark=correspondence_landmark,
                city=correspondence_city_instance,
                zip=correspondence_pin_code,
            )
            return Response(
                {
                    "message": "Employee Address is Successfully Created",
                    "success": True,
                },
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

    def put(self, request, pk=None):
        try:
            data = request.data
            # emp_id = data.get("emp_id")
            if not pk:
                raise ClientErrors("pk is required")

            obj_emp = PrimaryEmpInfo.objects.get(id=pk)
            queryset = AddressEmpInfo.objects.filter(emp=obj_emp)

            if not queryset.exists():
                raise ClientErrors(
                    "No address information found for the given employee"
                )

            # Update the existing address information
            for address_info in queryset:
                address_type = address_info.type.lower()
                if f"{address_type}_address_proof" in data:
                    address_proof = data[f"{address_type}_address_proof"]
                    address_proof_instance = UploadedFile.objects.create(
                        upload=address_proof, created_by=request.user
                    )
                    address_info.address_proof = address_proof_instance

                address_info.isVerified = data.get(
                    "isVerified", address_info.isVerified
                )
                address_info.is_both_address_same = data.get(
                    "is_both_address_same", address_info.is_both_address_same
                )
                address_info.address = data.get(
                    f"{address_type}_address", address_info.address
                )
                address_info.landmark = data.get(
                    f"{address_type}_landmark", address_info.landmark
                )
                address_info.zip = data.get(
                    f"{address_type}_pin_code", address_info.zip
                )

                city_id = data.get(f"{address_type}_city")
                city_instance = City.objects.get(pk=city_id)
                address_info.city = city_instance

                address_info.save()

            return Response(
                {
                    "message": "Employee Address is Successfully Updated",
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
