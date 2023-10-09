
from rest_framework import serializers
from mferp.address.models import City, Country, State


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


# class EventLocationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EventLocation
#         fields = '__all__'


# class AddressSerializer(serializers.ModelSerializer):
#     state = StateSerializer(source="city.state", read_only=True)
#     country = CountrySerializer(source="city.state.country", read_only=True)

#     class Meta:
#         model = Address
#         fields = ["id", "city", "state", "country", "event", "is_primary"]

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         city_name = instance.city.name
#         return {
#             "id": representation["id"],
#             "event_id": representation["event"],
#             "city_name": city_name,
#             "primary": representation["is_primary"],
#             "city_id": representation["city"],
#             "state_id": representation["state"]["id"],
#             "state_name": representation["state"]["name"],
#             "country_id": representation["country"]["id"],
#             "country_name": representation["country"]["name"],
#         }