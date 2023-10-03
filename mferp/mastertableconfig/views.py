from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MasterConfig, Organization
from .serializers import MasterConfigSerializer, OrganizationSerializer
from rest_framework import generics, mixins
from mferp.common.errors import ClientErrors, DatabaseErrors, UserErrors
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class CreateCategoryOrSubcategoryView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.UpdateModelMixin
):
    serializer_class = MasterConfigSerializer
    # permission_class = [IsAuthenticated]
    queryset = MasterConfig.objects.all()

    def patch(self, request, pk=None):
        try:
            return self.partial_update(request, pk, partial=True)

        except UserErrors as error:
            return Response(
                {"message": error.message, "success": False}, status=error.response_code
            )
        except Exception as error:
            return Response(
                {"message": "Something Went Wrong", "success": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, pk=None):
        try:
            return self.update(request, pk)
        except UserErrors as error:
            return Response(
                {"message": error.message, "success": False}, status=error.response_code
            )
        except Exception as error:
            return Response(
                {"message": "Something Went Wrong", "success": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        try:
            data = request.data
            serializer = MasterConfigSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"data": serializer.data, "success": True},
                    status=status.HTTP_201_CREATED,
                )

            return Response(
                {"data": serializer.errors, "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except UserErrors as error:
            return Response(
                {"message": error.message, "success": False}, status=error.response_code
            )
        except Exception as error:
            return Response(
                {"message": "Something Went Wrong", "success": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class OrganizationView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.UpdateModelMixin
):
    serializer_class = OrganizationSerializer
    # permission_class = [IsAuthenticated]
    queryset = Organization.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            if not "pk" in kwargs:
                return self.list(request)
            post = get_object_or_404(Organization, pk=kwargs["pk"])
            return Response(
                {"data": OrganizationSerializer(post).data, "success": True},
                status=status.HTTP_200_OK,
            )
        except UserErrors as error:
            return Response(
                {"message": error.message, "success": False}, status=error.response_code
            )
        except Exception as error:
            return Response(
                {"message": "Something Went Wrong", "success": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def patch(self, request, pk=None):
        try:
            try:
                instance = self.get_object()
            except Organization.DoesNotExist:
                return Response(
                    {"message": "Instance is not present", "success": False},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            foreign_fields = {
                "type_of_organization": "type_of_organization",
                "ownership_status": "ownership_status",
                "nature_of_organization": "nature_of_organization",
                "region": "region",
                "affiliated_university": "affiliated_university",
            }

            for request_key, model_field in foreign_fields.items():
                value = request.data.get(request_key)
                if value:
                    instance_value = MasterConfig.objects.get(pk=value)
                    setattr(instance, model_field, instance_value)

            instance.save()
            self.partial_update(request, pk, partial=True)
            return Response(
                {
                    "message": "Successfully Updated the data",
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )

        except UserErrors as error:
            return Response(
                {"message": error.message, "success": False}, status=error.response_code
            )
        except Exception as error:
            return Response(
                {"message": "Something Went Wrong", "success": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, pk=None, *args, **kwargs):
        try:
            try:
                instance = self.get_object()
            except Organization.DoesNotExist:
                return Response(
                    {"message": "Instance is not present", "success": False},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            foreign_fields = {
                "type_of_organization": "type_of_organization",
                "ownership_status": "ownership_status",
                "nature_of_organization": "nature_of_organization",
                "region": "region",
                "affiliated_university": "affiliated_university",
            }

            for request_key, model_field in foreign_fields.items():
                value = request.data.get(request_key)
                if value:
                    instance_value = MasterConfig.objects.get(pk=value)
                    setattr(instance, model_field, instance_value)

            instance.save()

            super().update(request, *args, **kwargs)
            return Response(
                {
                    "message": "Successfully Updated the data",
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )
        except UserErrors as error:
            return Response(
                {"message": error.args[0], "success": False}, status=error.response_code
            )
        except Exception as error:
            return Response(
                {"message": "Something Went Wrong", "success": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        try:
            data = request.data
            serializer = OrganizationSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"data": serializer.data, "success": True},
                    status=status.HTTP_201_CREATED,
                )

            return Response(
                {"data": serializer.errors, "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except UserErrors as error:
            return Response(
                {"message": error.message, "success": False}, status=error.response_code
            )
        except Exception as error:
            return Response(
                {"message": "Something Went Wrong", "success": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )





