from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from mferp.address.models import Country, State, City
from .models import MasterConfig, OrgAddress, Organization, Test
from mferp.upload.models import UploadedFile
from .serializers import (
    MasterConfigSerializer,
    OrganizationSerializer,
    OrgAddressSerializer,TestSerializer
)
from rest_framework import generics, mixins
from mferp.common.errors import ClientErrors, DatabaseErrors, UserErrors
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from mferp.common.functions import get_date_datetime, get_string_datetime


class CreateCategoryOrSubcategoryView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.UpdateModelMixin
):
    serializer_class = MasterConfigSerializer
    permission_classes = [IsAuthenticated]
    queryset = MasterConfig.objects.all()

    def patch(self, request, pk=None):
        try:
            self.partial_update(request, pk, partial=True)
            return Response(
                {
                    "message": "data is updatated ",
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

    # def put(self, request, pk=None):
    #     try:
    #         return self.update(request, pk)
    #     except UserErrors as error:
    #         return Response(
    #             {"message": error.message, "success": False}, status=error.response_code
    #         )
    #     except Exception as error:
    #         return Response(
    #             {"message": "Something Went Wrong", "success": False},
    #             status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         )

    def post(self, request):
        try:
            data = request.data
            serializer = MasterConfigSerializer(data=data)
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
                {"message": "Category is Successfully Created", "success": True},
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


class OrganizationView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.UpdateModelMixin
):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]
    queryset = Organization.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            organizations = Organization.objects.all()
            combined_data = []

            for org in organizations:
                org_serializer = OrganizationSerializer(org)
                addresses = OrgAddress.objects.filter(organization=org)
                address_serializer = OrgAddressSerializer(addresses, many=True)

                org_data = org_serializer.data
                org_data["address"] = address_serializer.data

                combined_data.append(org_data)
            return Response(
                {
                    "data": combined_data,
                    "success": True,
                    "status": status.HTTP_200_OK,
                },
            )
        except UserErrors as error:
            return Response(
                {
                    "message": error.message,
                    "success": False,
                    "status": error.response_code,
                }
            )
        except Exception as error:
            return Response(
                {
                    "message": "Something Went Wrong",
                    "success": False,
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                }
            )

    # def get(self, request, *args, **kwargs):
    #     try:
    #         if not "pk" in kwargs:
    #             return self.list(request)
    #         post = get_object_or_404(Organization, pk=kwargs["pk"])
    #         return Response(
    #             {"data": OrganizationSerializer(post).data, "success": True},
    #             status=status.HTTP_200_OK,
    #         )
    #     except UserErrors as error:
    #         return Response(
    #             {"message": error.message, "success": False}, status=error.response_code
    #         )
    #     except Exception as error:
    #         return Response(
    #             {"message": "Something Went Wrong", "success": False},
    #             status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         )

    # def patch(self, request, pk=None):
    #     try:
    #         try:
    #             instance = self.get_object()
    #         except Organization.DoesNotExist:
    #             return Response(
    #                 {"message": "Instance is not present", "success": False},
    #                 status=status.HTTP_400_BAD_REQUEST,
    #             )
    #         foreign_fields = {
    #             "type_of_organization": "type_of_organization",
    #             "ownership_status": "ownership_status",
    #             "nature_of_organization": "nature_of_organization",
    #             "region": "region",
    #             "affiliated_university": "affiliated_university",
    #         }

    #         for request_key, model_field in foreign_fields.items():
    #             value = request.data.get(request_key)
    #             if value:
    #                 instance_value = MasterConfig.objects.get(pk=value)
    #                 setattr(instance, model_field, instance_value)

    #         instance.save()
    #         self.partial_update(request, pk, partial=True)
    #         return Response(
    #             {
    #                 "message": "Successfully Updated the data",
    #                 "success": True,
    #             },
    #             status=status.HTTP_200_OK,
    #         )

    #     except UserErrors as error:
    #         return Response(
    #             {"message": error.message, "success": False}, status=error.response_code
    #         )
    #     except Exception as error:
    #         return Response(
    #             {"message": "Something Went Wrong", "success": False},
    #             status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         )

    # def put(self, request, pk=None, *args, **kwargs):
    #     try:
    #         try:
    #             instance = self.get_object()
    #         except Organization.DoesNotExist:
    #             return Response(
    #                 {"message": "Instance is not present", "success": False},
    #                 status=status.HTTP_400_BAD_REQUEST,
    #             )
    #         foreign_fields = {
    #             "type_of_organization": "type_of_organization",
    #             "ownership_status": "ownership_status",
    #             "nature_of_organization": "nature_of_organization",
    #             "region": "region",
    #             "affiliated_university": "affiliated_university",
    #         }

    #         for request_key, model_field in foreign_fields.items():
    #             value = request.data.get(request_key)
    #             if value:
    #                 instance_value = MasterConfig.objects.get(pk=value)
    #                 setattr(instance, model_field, instance_value)

    #         instance.save()

    #         super().update(request, *args, **kwargs)
    #         return Response(
    #             {
    #                 "message": "Successfully Updated the data",
    #                 "success": True,
    #             },
    #             status=status.HTTP_200_OK,
    #         )
    #     except UserErrors as error:
    #         return Response(
    #             {"message": error.args[0], "success": False}, status=error.response_code
    #         )
    #     except Exception as error:
    #         return Response(
    #             {"message": "Something Went Wrong", "success": False},
    #             status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         )

    def post(self, request):
        try:
            data = request.data
            if ("child_count") not in request.data:
                raise ClientErrors(message="All fields are required", response_code=400)
            child_count = int(request.data.get("child_count"))
            for assign in range(0, child_count + 1):
                if ("org_type_" + str(assign)) not in request.data:
                    raise ClientErrors("All field required")
                if ("ownership_status_" + str(assign)) not in request.data:
                    raise ClientErrors("All field required")
                if ("org_nature_" + str(assign)) not in request.data:
                    raise ClientErrors("All field required")
                if ("region_" + str(assign)) not in request.data:
                    raise ClientErrors("All field required")
                if ("affiliated_university_" + str(assign)) not in request.data:
                    raise ClientErrors("All field required")
                if ("establishment_date_" + str(assign)) not in request.data:
                    raise ClientErrors("All field required")
                if ("address_" + str(assign)) not in request.data:
                    raise ClientErrors("All field required")
                # if ("country_" + str(assign)) not in request.data:
                #     raise ClientErrors("All field required")
                # if ("state_" + str(assign)) not in request.data:
                #     raise ClientErrors("All field required")
                if ("city_" + str(assign)) not in request.data:
                    raise ClientErrors("All field required")
                if ("pin_code_" + str(assign)) not in request.data:
                    raise ClientErrors("All field required")
                if ("email_" + str(assign)) not in request.data:
                    raise ClientErrors("All field required")
                if ("phone_number_" + str(assign)) not in request.data:
                    raise ClientErrors("All field required")
            for assign in range(0, child_count + 1):
                org_type = data.get("org_type_" + str(assign))
                org_name = data.get("org_name_" + str(assign))
                ownership_status = data.get("ownership_status_" + str(assign))
                org_nature = data.get("org_nature_" + str(assign))
                region = data.get("region_" + str(assign))
                affiliated_university = data.get("affiliated_university_" + str(assign))
                establishment_date = get_date_datetime(
                    data.get("establishment_date_" + str(assign))
                )
                org_short_code = data.get("org_short_code_" + str(assign), None)
                org_logo = data.get("org_logo_" + str(assign), None)
                org_cover_banner = data.get("org_cover_banner_" + str(assign), None)
                org_photo = data.get("org_photo_" + str(assign), None)
                address = data.get("address_" + str(assign))
                # country = data.get("country_" + str(assign), None)
                city = data.get("city_" + str(assign), None)
                landmark = data.get("landmark_" + str(assign), None)
                pin_code = data.get("pin_code_" + str(assign))
                web_address = data.get("web_address_" + str(assign), None)
                email = data.get("email_" + str(assign))
                contact_number = data.get("contact_number_" + str(assign), None)
                phone_number = data.get("phone_number_" + str(assign))
                # state = data.get("state_" + str(assign))

                instance_org_type = MasterConfig.objects.get(pk=org_type)
                ownership_master = MasterConfig.objects.get(pk=ownership_status)
                instance_nature = MasterConfig.objects.get(pk=org_nature)
                instance_region = MasterConfig.objects.get(pk=region)
                instance_affiliated = MasterConfig.objects.get(pk=affiliated_university)

                # country_instance = Country.objects.get(pk=country)
                # state_instance = State.objects.get(pk=state)
                city_instance = City.objects.get(pk=city)

                if assign == 0:
                    obj = Organization.objects.create(
                        type_of_organization=instance_org_type,
                        org_name=org_name,
                        ownership_status=ownership_master,
                        nature_of_organization=instance_nature,
                        affiliated_university=instance_affiliated,
                        establishment_date=establishment_date,
                        short_code=org_short_code,
                        logo_org=org_logo,
                        cover_banner_org=org_cover_banner,
                        photo_org=org_photo,
                    )
                    OrgAddress.objects.create(
                        organization=obj,
                        region=instance_region,
                        address=address,
                        landmark=landmark,
                        zip=pin_code,
                        city=city_instance,
                        web_address=web_address,
                        email=email,
                        contact_number=contact_number,
                        phone_number=phone_number,
                    )

                else:
                    child_obj = Organization.objects.create(
                        type_of_organization=instance_org_type,
                        org_name=org_name,
                        ownership_status=ownership_master,
                        nature_of_organization=instance_nature,
                        affiliated_university=instance_affiliated,
                        establishment_date=establishment_date,
                        short_code=org_short_code,
                        logo_org=org_logo,
                        cover_banner_org=org_cover_banner,
                        photo_org=org_photo,
                        parent=obj,
                    )
                    OrgAddress.objects.create(
                        organization=child_obj,
                        region=instance_region,
                        address=address,
                        landmark=landmark,
                        zip=pin_code,
                        city=city_instance,
                        web_address=web_address,
                        email=email,
                        contact_number=contact_number,
                        phone_number=phone_number,
                    )
            return Response(
                {
                    "message": "Organisation Successfully Created",
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

class TestView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
):
    serializer_class = TestSerializer
    # permission_classes = [IsAuthenticated]
    queryset = UploadedFile.objects.all()

    # group_required('hr_configuration')
    # @group_required('hr_configuration')
    # def get(self, request, *args, **kwargs):
    #     try:
    #         if not "pk" in kwargs:
    #             return self.list(request)
    #         post = get_object_or_404(Employee, pk=kwargs["pk"])
    #         return Response(
    #             {
    #                 "data": EmployeeSerializer(post).data,
    #                 "success": True,
    #             },
    #             status=status.HTTP_200_OK,
    #         )
    #     except Exception as error:
    #         return Response(
    #             {
    #                 "message": "Something Went Wrong",
    #                 "success": False,
    #             },
    #             status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         )

    def post(self, request):
        try:
            data = request.data
            # serializer = TestSerializer(data=data)
            # if "name" or "image" not in request.data:
            #     raise ClientErrors("All Fields are required")
            image = data["image"]
            name = data["name"]
            print(name,image)
            obj = UploadedFile.objects.create(upload=image) 
            obj2 = Test.objects.create(name=name, cover_image=obj)
            # if serializer.is_valid():
            #     post = serializer.save()
            return Response(
                {
                    "message": "Employee Successfully Created",
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
        
