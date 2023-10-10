from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, mixins
from .models import Country, State, City
from .serializers import CountrySerializer, StateSerializer, CitySerializer
from rest_framework.views import APIView

from mferp.common.errors import ClientErrors, DatabaseErrors, UserErrors
from django.shortcuts import get_object_or_404


class CountryAPIView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = CountrySerializer
    # permission_class = [IsAuthenticated]
    queryset = Country.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            return self.list(request)
        except UserErrors as error:
            return Response(
                {"message": error.message, "success": False}, status=error.response_code
            )
        except Exception as error:
            return Response(
                {"message": "Something Went Wrong", "success": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        

class GetStateAPIView(APIView):
    serializer_class = StateSerializer
    # permission_class = [IsAuthenticated]
    queryset = State.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            params = request.query_params
            country_id = params.get("country_id")
            if not country_id:
                raise ClientErrors(message="No country id provided", response_code=400)
            country = get_object_or_404(Country, pk=country_id)
            queryset = State.objects.filter(country=country)
            return Response(
                {"data": StateSerializer(queryset, many=True).data, "success": True},
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
        

class GetCityAPIView(APIView):
    serializer_class = CitySerializer
    # permission_class = [IsAuthenticated]
    queryset = City.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            params = request.query_params
            state_id = params.get("state_id")
            if not state_id:
                raise ClientErrors(message="No state id provided", response_code=400)
            state = get_object_or_404(State, pk=state_id)
            queryset = City.objects.filter(state=state)
            return Response(
                {"data": CitySerializer(queryset, many=True).data, "success": True},
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